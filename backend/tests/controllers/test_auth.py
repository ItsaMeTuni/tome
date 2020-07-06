import time
import uuid
from datetime import datetime, timedelta

import asyncpg
import jwt
import pytest

from tome.exceptions import HTTPException
from tome.models.user import User
from tome.utils import ORJSONCodec

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


async def test_api_key(db: asyncpg.Connection, monkeypatch):
    import tome.controllers.auth
    import tome.models.user

    user = await _create_test_user(db)
    monkeypatch.setattr(
        tome.controllers.auth, "ALLOWED_API_KEY_SCOPES", frozenset({"foo", "bar"})
    )
    exp = datetime.now() + timedelta(hours=1)
    key = await tome.controllers.auth.create_api_key(exp, user, ["foo", "bar"])
    result = await tome.controllers.auth.validate_api_key(key)
    assert result == (user, ["foo", "bar"])

    with pytest.raises(HTTPException) as exc_info:
        await tome.controllers.auth.create_api_key(exp, user, ["foo", "not_allowed"])
    assert exc_info.value.status_code == 422

    with pytest.raises(HTTPException) as exc_info:
        await tome.controllers.auth.validate_api_key(uuid.uuid4())

    assert exc_info.value.status_code == 401

    exp = datetime.now() - timedelta(hours=1)
    key = await tome.controllers.auth.create_api_key(exp, user, ["foo", "bar"])

    with pytest.raises(HTTPException) as exc_info:
        await tome.controllers.auth.validate_api_key(key)

    assert exc_info.value.status_code == 401


async def test_auth_token(db: asyncpg.Connection):
    import tome.controllers.auth

    user = await _create_test_user(db)

    auth_token = await tome.controllers.auth.get_auth_token(user, ["foo", "bar"])

    result = await tome.controllers.auth.validate_auth_token(auth_token.encode())
    assert result == (user, ["foo", "bar"])

    with pytest.raises(HTTPException) as exc_info:
        await tome.controllers.auth.validate_auth_token(auth_token.encode()[:-7])

    assert exc_info.value.status_code == 401

    now = time.time()
    expired_auth_token = jwt.encode(
        {
            "sub": user.id,
            "iat": now,
            "nbf": now,
            "exp": now - 10000,
            "iss": tome.controllers.auth.ISSUER,
            "aud": tome.controllers.auth.AUDIENCE,
        },
        key=tome.controllers.auth.SECRET_KEY,
        json_encoder=ORJSONCodec,
    ).decode()

    with pytest.raises(HTTPException) as exc_info:
        await tome.controllers.auth.validate_auth_token(expired_auth_token)

    assert exc_info.value.status_code == 401

    await db.execute("delete from users where id = $1", user.id)

    with pytest.raises(HTTPException) as exc_info:
        await tome.controllers.auth.validate_auth_token(auth_token.encode())

    assert exc_info.value.status_code == 409
