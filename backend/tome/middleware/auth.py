import functools
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple
from uuid import UUID

from starlette.requests import HTTPConnection, Request
from starlette.responses import RedirectResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.websockets import WebSocket

from tome.controllers import auth
from tome.exception_handlers import handle_http_exception
from tome.exceptions import HTTPException
from tome.models.user import User


class AuthenticationMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            request = Request(scope, receive, send)
            try:
                scope["user"], scope["auth"] = await self.authenticate(request)
            except HTTPException as e:
                response = await handle_http_exception(request, e)
                await response(scope, receive, send)
                return
        elif scope["type"] == "websocket":
            sock = WebSocket(scope, receive, send)
            try:
                scope["user"], scope["auth"] = await self.authenticate(sock)
            except HTTPException as e:
                await send({"type": "websocket.close", "code": 3700 + e.status_code})
                return
        await self.app(scope, receive, send)

    async def authenticate(
        self, request: HTTPConnection
    ) -> Tuple[Optional[User], List[str]]:
        header: str = request.headers.get("Authorization", "")
        prefix, _, token = header.partition(" ")
        if prefix != "Bearer":
            return None, ["anonymous"]
        if token.startswith("api-key-"):
            try:
                uuid = UUID(token[8:])
            except ValueError as e:
                raise HTTPException("invalid API key", 401) from e
            return await auth.validate_api_key(uuid)
        else:
            # token is JWT
            return await auth.validate_auth_token(token.encode())


def requires(
    *scopes: str,
    status_code: int = None,
    detail: Any = "forbidden",
    headers: Optional[Dict[str, str]] = None,
    redirect: Optional[str] = None
) -> Callable[
    [Callable[[Request], Awaitable[Response]]], Callable[[Request], Awaitable[Response]]
]:
    scopes_set = set(scopes)

    def decorator(
        endpoint: Callable[[Request], Awaitable[Response]]
    ) -> Callable[[Request], Awaitable[Response]]:
        if redirect is None:
            exc = HTTPException(
                detail=detail, status_code=status_code or 401, headers=headers
            )

            async def inner(request: Request) -> Response:
                if scopes_set - set(request.auth):
                    raise exc
                return await endpoint(request)

        else:
            response = RedirectResponse(
                redirect, status_code=status_code or 307, headers=headers
            )

            async def inner(request: Request) -> Response:
                if scopes_set - set(request.auth):
                    return response
                else:
                    return await endpoint(request)

        return functools.wraps(endpoint)(inner)

    return decorator
