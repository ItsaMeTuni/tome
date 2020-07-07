import starlette.requests

from tome.controllers.auth import get_auth_token
from tome.database import connection
from tome.models.user import User
from tome.responses import ORJSONResponse
from tome.routing import post
from tome.utils import get_json, validate_types_raising


@post("/api/auth/login")
async def login(request: starlette.requests.Request) -> ORJSONResponse:
    """logs the user in with email and password, returning an auth token"""
    json = await get_json(request)
    validate_types_raising(json, {"email": str, "password": str})
    user = User(
        **await connection().fetchrow(
            "select id, password from users where email = $1", json["email"]
        )
    )
    return ORJSONResponse(get_auth_token(user, ["user/read", "user/write"]))


routes = [login]
