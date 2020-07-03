from starlette.requests import Request

from tome.exceptions import HTTPException
from tome.responses import ORJSONResponse


async def handle_http_exception(
    _request: Request, exception: HTTPException
) -> ORJSONResponse:
    """handles our custom HTTPException with headers"""
    return ORJSONResponse(
        {"error": exception.detail},
        headers=exception.headers,
        status_code=exception.status_code,
    )
