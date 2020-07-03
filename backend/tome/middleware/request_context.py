from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

request: ContextVar[Request] = ContextVar("request")


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request_: Request, call_next: RequestResponseEndpoint, /  # noqa W504
    ) -> Response:
        token = request.set(request_)
        response = await call_next(request_)
        # TODO(pxeger): is this needed? maybe asyncio does this automatically?
        request.reset(token)
        return response
