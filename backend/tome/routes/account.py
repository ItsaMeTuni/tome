import email_validator
from starlette.requests import Request

from tome.database import connection
from tome.exceptions import HTTPException
from tome.middleware.auth import requires
from tome.responses import ORJSONResponse
from tome.routing import delete, get, patch
from tome.utils import get_json, validate_types_raising


@get("/api/me")
@requires("account.read")
async def get_account(request: Request) -> ORJSONResponse:
    return ORJSONResponse(request.user.__dict__)


@patch("/api/me/name")
@requires("account.write.name")
async def patch_account(request: Request) -> ORJSONResponse:
    name = await get_json(request)
    validate_types_raising(name, str)
    if not name:
        raise HTTPException("invalid name", 400)
    await connection().execute(
        "update users set name = $1 where id = $2", name, request.user.id
    )
    return ORJSONResponse()


@patch("/api/me/email")
@requires("account.write.email")
async def patch_account_email(request: Request) -> ORJSONResponse:
    json = await get_json(request)
    validate_types_raising(json, str)
    try:
        email = email_validator.validate_email(json).email
    except email_validator.EmailNotValidError as e:
        raise HTTPException("invalid email address", 400) from e
    await connection().execute(
        "update users set email = $1 where id = $2", email, request.user.id
    )
    return ORJSONResponse()


@delete("/api/me")
@requires("account.delete")
async def patch_account_email(request: Request) -> ORJSONResponse:
    conn = connection()
    async with conn.transaction():
        await conn.execute(
            "delete from api_keys where user_id = $1;"
            "delete from users where id = $1;",
            request.user.id,
        )
    return ORJSONResponse(None, 205)
