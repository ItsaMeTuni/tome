import uuid
from unittest.mock import AsyncMock

import asyncpg
import pytest
from starlette.datastructures import MutableHeaders

from tome.exceptions import HTTPException
from tome.models.user import User

pytestmark = pytest.mark.asyncio


async def _create_test_user(db: asyncpg.Connection) -> User:
    user = User(id=uuid.uuid4(), name="foo bar", email="foobar@example.com")

    await db.execute(
        """insert into users (id, email, name, password) values ($1, $2, $3, $4)""",
        user.id,
        user.email,
        user.name,
        "hunter2",
    )

    return user


async def test_auth_middleware_call(monkeypatch):
    import tome.middleware.auth

    fake_user = object()
    fake_auth = object()
    fake_app = AsyncMock()
    fake_receive = AsyncMock()
    fake_send = AsyncMock()

    async def fake_authenticate_correct(_self, _request):
        return fake_user, fake_auth

    monkeypatch.setattr(
        tome.middleware.auth.AuthenticationMiddleware,
        "authenticate",
        fake_authenticate_correct,
    )

    middleware = tome.middleware.auth.AuthenticationMiddleware(fake_app)

    scope = {"type": "fake"}  # other events should be passed straight through to app
    await middleware(scope, fake_receive, fake_send)
    fake_app.assert_awaited_once_with(scope, fake_receive, fake_send)
    fake_send.assert_not_awaited()
    fake_receive.assert_not_awaited()

    fake_app.reset_mock()
    scope = {"type": "http"}
    await middleware(scope, fake_receive, fake_send)
    fake_app.assert_awaited_once_with(scope, fake_receive, fake_send)
    assert scope["user"] == fake_user
    assert scope["auth"] == fake_auth

    fake_app.reset_mock()
    scope = {"type": "websocket"}
    await middleware(scope, fake_receive, fake_send)
    fake_app.assert_awaited_once_with(scope, fake_receive, fake_send)
    assert scope["user"] == fake_user
    assert scope["auth"] == fake_auth

    async def fake_authenticate_incorrect(_self, _request):
        raise HTTPException("foo bar", 418)

    monkeypatch.setattr(
        tome.middleware.auth.AuthenticationMiddleware,
        "authenticate",
        fake_authenticate_incorrect,
    )

    fake_app.reset_mock()
    scope = {"type": "http"}
    await middleware(scope, fake_receive, fake_send)
    fake_app.assert_not_awaited()

    fake_app.reset_mock()
    fake_send.reset_mock()
    scope = {"type": "websocket"}
    await middleware(scope, fake_receive, fake_send)
    # http code 4xx -> ws code 41xx)
    fake_send.assert_awaited_once_with({"type": "websocket.close", "code": 4118})
    fake_app.assert_not_awaited()


async def test_authenticate(monkeypatch):
    import tome.middleware.auth

    fake_app = AsyncMock()
    fake_validate_api_key = AsyncMock()
    fake_validate_auth_token = AsyncMock()

    middleware = tome.middleware.auth.AuthenticationMiddleware(fake_app)
    monkeypatch.setattr(
        tome.middleware.auth.auth, "validate_api_key", fake_validate_api_key
    )
    monkeypatch.setattr(
        tome.middleware.auth.auth, "validate_auth_token", fake_validate_auth_token
    )

    fake_request = type("", (), {})()
    fake_request.headers = MutableHeaders({})
    assert await middleware.authenticate(fake_request) == (None, ["anonymous"])

    fake_request.headers["authorization"] = "fake"
    assert await middleware.authenticate(fake_request) == (None, ["anonymous"])

    key = uuid.uuid4()
    fake_request.headers["authorization"] = "Bearer api-key-" + key.hex
    await middleware.authenticate(fake_request)
    fake_validate_api_key.assert_awaited_once_with(key)
    fake_validate_auth_token.assert_not_awaited()

    with pytest.raises(HTTPException) as exc_info:
        fake_request.headers["authorization"] = "Bearer api-key-invalid"
        await middleware.authenticate(fake_request)

    assert exc_info.value.status_code == 401

    fake_validate_api_key.reset_mock()
    fake_validate_auth_token.reset_mock()
    fake_request.headers["authorization"] = "Bearer foobar-auth-token"
    await middleware.authenticate(fake_request)
    fake_validate_api_key.assert_not_awaited()
    fake_validate_auth_token.assert_awaited_once_with(b"foobar-auth-token")


async def test_requires():
    from tome.middleware.auth import requires

    @requires("foo", "bar", headers={"x-eggs": "spam"})
    async def route(_request):
        return "fake response"

    fake_request = type("", (), {})()

    fake_request.auth = ["foo", "bar"]
    await route(fake_request)

    fake_request.auth = ["foo", "bar", "extra"]
    await route(fake_request)

    fake_request.auth = ["foo"]
    with pytest.raises(HTTPException) as exc_info:
        await route(fake_request)
    assert exc_info.value.status_code == 401

    @requires("foo", "bar", headers={"x-eggs": "spam"}, status_code=418)
    async def route(_request):
        return "fake response"

    with pytest.raises(HTTPException) as exc_info:
        await route(fake_request)
    assert exc_info.value.status_code == 418

    @requires(
        "foo", "bar", redirect="https://example.com/foobar", headers={"x-spam": "eggs"}
    )
    async def route(_request):
        return "fake response"

    fake_request.auth = ["foo", "bar", "extra"]
    assert await route(fake_request) == "fake response"

    fake_request.auth = ["foo"]
    response = await route(fake_request)
    assert response.headers["location"] == "https://example.com/foobar"
    assert response.headers["x-spam"] == "eggs"
    assert response.status_code == 307

    @requires(
        "foo",
        "bar",
        redirect="https://example.com/foobar",
        headers={"x-spam": "eggs"},
        status_code=318,
    )
    async def route(_request):
        return "fake response"

    assert (await route(fake_request)).status_code == 318
