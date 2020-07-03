import time
from typing import List, Optional

from starlette.requests import Request

from tome.controllers.auth import create_api_key
from tome.middleware.auth import requires
from tome.responses import ORJSONResponse
from tome.routing import post
from tome.utils import get_json, validate_types_raising


@post("/api/account/api_token")
@requires("account.api_token.generate")
async def generate_api_token(request: Request) -> ORJSONResponse:
    json = await get_json(request)
    validate_types_raising(json, {"scope": List[str], "duration": Optional[int]})
    if json["duration"] is not None:
        expiry = time.time() + json["duration"]
    else:
        expiry = None
    scope = json["scope"]
    key = await create_api_key(expiry, request.user, scope)
    return ORJSONResponse(key, 201)


routes = [generate_api_token]
