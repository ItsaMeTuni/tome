import asyncio

from httpx import AsyncClient
from starlette.applications import Starlette
from starlette.responses import Response


def test_request_context():
    from tome.middleware.request_context import (
        RequestContextMiddleware,
        request as request2,
    )

    app = Starlette()
    app.add_middleware(RequestContextMiddleware)

    @app.route("/")
    async def route(request1):
        assert request1 == request2.get()
        return Response()

    async def _test():
        client = AsyncClient(app=app, base_url="http://testserver")
        await client.get("/")

    asyncio.run(_test())
