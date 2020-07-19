import starlette.requests

from tome.controllers.auth import get_auth_token
from tome.controllers.password import verify_password
from tome.database import connection
from tome.exceptions import HTTPException
from tome.middleware.auth import requires
from tome.responses import ORJSONResponse
from tome.routing import post
from tome.utils import get_json, validate_types_raising

LOGIN_SCOPES = [
    "account.read",
    "account.write.email",
    "account.write.name",
    "account.delete",
    "account.password",
    "account.api_key.get",
    "account.api_key.generate",
    "account.api_key.delete",
    "refresh",
]


@post("/api/auth/login")
async def login(request: starlette.requests.Request) -> ORJSONResponse:
    """logs the user in with email and password, returning an auth token"""
    json = await get_json(request)
    validate_types_raising(json, {"email": str, "password": str})
    row = await connection().fetchrow(
        "select id, password from users where email = $1", json["email"]
    )
    if not (row and verify_password(row["password"], json["password"])):
        raise HTTPException("Incorrect username or password", 401)
    return ORJSONResponse(await get_auth_token(row["id"], LOGIN_SCOPES))


@post("/api/auth/refresh")
@requires("refresh")
async def refresh(request: starlette.requests.Request) -> ORJSONResponse:
    """refreshes an auth token"""
    return ORJSONResponse(await get_auth_token(request.user.id, request.auth))


routes = [login]
