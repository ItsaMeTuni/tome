from starlette.types import ASGIApp, Receive, Scope, Send

from tome.responses import ORJSONResponse


class ServerErrorMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # noinspection PyBroadException
        try:
            return await self.app(scope, receive, send)
        except Exception:
            response = ORJSONResponse(
                {"error": "internal server error"},
                status_code=500
            )
            await response(scope, receive, send)
