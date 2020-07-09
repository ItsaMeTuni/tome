import time
from typing import List, Optional

from starlette.requests import Request

from tome.controllers.auth import create_api_key
from tome.database import connection
from tome.exceptions import HTTPException
from tome.middleware.auth import requires
from tome.responses import ORJSONResponse
from tome.routing import delete, get, post
from tome.utils import get_json, validate_types_raising


@post("/api/account/api_key")
@requires("account.api_key.generate")
async def generate_api_key(request: Request) -> ORJSONResponse:
    json = await get_json(request)
    validate_types_raising(json, {"scope": List[str], "duration": Optional[int]})
    if json["duration"] is not None:
        expiry = time.time() + json["duration"]
    else:
        expiry = None
    scope = json["scope"]
    key = await create_api_key(expiry, request.user, scope)
    return ORJSONResponse(key, 201)


@delete("/api/account/api_key")
@requires("account.api_key.delete")
async def delete_api_key(request: Request) -> ORJSONResponse:
    validate_types_raising(request.query_params, {"id": str})
    result = await connection().execute(
        "delete from api_keys where id = $1 and user_id = $2",
        request.query_params["id"],
        request.user.id,
    )
    if result.split(" ")[1] == "0":
        raise HTTPException("not found", 404)
    return ORJSONResponse()


@get("/api/account/api_key")
@requires("account.api_key.get")
async def get_api_key(request: Request) -> ORJSONResponse:
    if "id" in request.query_params:
        result = await connection().fetch(
            "select id, scope, expiry from api_keys where id = $1 and user_id = $2",
            request.query_params["id"],
            request.user.id,
        )
        if not result:
            raise HTTPException("not found", 404)
    else:
        result = dict(
            await connection().fetchrow(
                "select id, scope, expiry from api_keys where user_id = $1",
                request.user.id,
            )
        )
    return ORJSONResponse(result)


routes = [generate_api_key, get_api_key, delete_api_key]
