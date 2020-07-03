from typing import Awaitable, Callable, List, Optional

from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from tome.responses import ORJSONResponse


def route(
    path: str,
    /,
    *,
    methods: Optional[List[str]] = None,
    name: Optional[str] = None,
    include_in_schema: bool = True,
) -> Callable[[Callable[[Request], Awaitable[Response]]], Route]:
    """decorator to convert an endpoint function/class into a Starlette Route object."""

    def decorator(endpoint: Callable[[Request], Awaitable[Response]]) -> Route:
        return Route(
            path,
            endpoint,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )

    return decorator


# helper decorators, setting route methods appropriately


def get(
    path: str, /, *, name: Optional[str] = None, include_in_schema: bool = True
) -> Callable[[Callable[[Request], Awaitable[Response]]], Route]:
    """decorator to create a Starlette Route for GET requests from an endpoint"""
    return route(path, methods=["GET"], name=name, include_in_schema=include_in_schema)


def post(
    path: str, /, *, name: Optional[str] = None, include_in_schema: bool = True
) -> Callable[[Callable[[Request], Awaitable[Response]]], Route]:
    """decorator to create a Starlette Route for POST requests from an endpoint"""
    return route(path, methods=["POST"], name=name, include_in_schema=include_in_schema)


def put(
    path: str, /, *, name: Optional[str] = None, include_in_schema: bool = True
) -> Callable[[Callable[[Request], Awaitable[Response]]], Route]:
    """decorator to create a Starlette Route for PUT requests from an endpoint"""
    return route(path, methods=["PUT"], name=name, include_in_schema=include_in_schema)


def patch(
    path: str, /, *, name: Optional[str] = None, include_in_schema: bool = True
) -> Callable[[Callable[[Request], Awaitable[Response]]], Route]:
    """decorator to create a Starlette Route for PATH requests from an endpoint"""
    return route(
        path, methods=["PATCH"], name=name, include_in_schema=include_in_schema
    )


def delete(
    path: str, /, *, name: Optional[str] = None, include_in_schema: bool = True
) -> Callable[[Callable[[Request], Awaitable[Response]]], Route]:
    """decorator to create a Starlette Route for DELETE requests from an endpoint"""
    return route(
        path, methods=["DELETE"], name=name, include_in_schema=include_in_schema
    )


def head(
    path: str, /, *, name: Optional[str] = None, include_in_schema: bool = True
) -> Callable[[Callable[[Request], Awaitable[Response]]], Route]:
    """decorator to create a Starlette Route for HEAD requests from an endpoint"""
    return route(path, methods=["HEAD"], name=name, include_in_schema=include_in_schema)


def options(
    path: str, /, *, name: Optional[str] = None, include_in_schema: bool = True
) -> Callable[[Callable[[Request], Awaitable[Response]]], Route]:
    """decorator to create a Starlette Route for OPTIONS requests from an endpoint"""
    return route(
        path, methods=["OPTIONS"], name=name, include_in_schema=include_in_schema
    )


@get("/api/")
async def index(_request: Request) -> ORJSONResponse:
    return ORJSONResponse("hello, world!")
