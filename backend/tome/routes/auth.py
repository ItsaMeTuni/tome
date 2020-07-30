import pyotp
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
    "account.two_factor",
    "refresh",
]

TWO_FACTOR_UPGRADE_TIME = 300  # seconds you have to complete login with 2fa


@post("/api/auth/login")
async def login(request: starlette.requests.Request) -> ORJSONResponse:
    """logs the user in with email and password, returning an auth token"""
    json = await get_json(request)
    validate_types_raising(json, {"email": str, "password": str})
    row = await connection().fetchrow(
        "select * from users where email = $1", json["email"]
    )
    if not (row and verify_password(row["password"], json["password"])):
        raise HTTPException("Incorrect username or password", 401)

    if row["two_factor_recovery"]:
        # 2fa is enabled
        token = await get_auth_token(
            row["id"], ["two_factor_upgrade"], TWO_FACTOR_UPGRADE_TIME
        )
        return ORJSONResponse({"token": token, "needs_two_factor_upgrade": True})

    token = await get_auth_token(row["id"], LOGIN_SCOPES)
    return ORJSONResponse({"token": token, "needs_two_factor_upgrade": False})


@post("/api/auth/two_factor_upgrade")
@requires("two_factor_upgrade")
async def two_factor_upgrade(request: starlette.requests.Request) -> ORJSONResponse:
    json = await get_json(request)
    validate_types_raising(json, str)

    totp = pyotp.TOTP(request.user.two_factor_secret)
    if totp.verify(json):
        return ORJSONResponse(await get_auth_token(request.user.id, LOGIN_SCOPES))

    elif json == request.user.two_factor_recovery:
        # TODO(pxeger) get them a new recovery code - email? frontend notification?
        return ORJSONResponse(await get_auth_token(request.user.id, LOGIN_SCOPES))

    else:
        raise HTTPException("Invalid two-factor authentication code", 401)


@post("/api/auth/refresh")
@requires("refresh")
async def refresh(request: starlette.requests.Request) -> ORJSONResponse:
    """refreshes an auth token"""
    return ORJSONResponse(await get_auth_token(request.user.id, request.auth))


routes = [login, two_factor_upgrade]
