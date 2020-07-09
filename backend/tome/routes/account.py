import email_validator
from starlette.requests import Request

from tome.controllers.password import hash_password, strength, verify_password
from tome.database import connection
from tome.exceptions import HTTPException
from tome.middleware.auth import requires
from tome.responses import ORJSONResponse
from tome.routing import delete, get, patch, post
from tome.utils import get_json, validate_types_raising


@get("/api/me")
@requires("account.read")
async def get_account(request: Request) -> ORJSONResponse:
    return ORJSONResponse(request.user.__dict__)


@patch("/api/me/name")
@requires("account.write.name")
async def patch_account_name(request: Request) -> ORJSONResponse:
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
async def delete_account(request: Request) -> ORJSONResponse:
    conn = connection()
    async with conn.transaction():
        await conn.execute(
            "delete from api_keys where user_id = $1;"
            "delete from users where id = $1;",
            request.user.id,
        )
    return ORJSONResponse(None, 205)


@post("/api/password")
@requires("account.password")
async def change_password(request: Request) -> ORJSONResponse:
    json = await get_json(request)
    validate_types_raising(json, {"new": str, "current": str})

    # check new password validity
    if json["new"] == json["current"]:
        # same as current (even if current is incorrect, we needn't bother checking)
        raise HTTPException("Password not changed", 422)
    elif json["new"] == "beef stew":
        # easter egg
        raise HTTPException("Password not stroganoff", 418)
    elif strength(json["new"]) < 8:
        raise HTTPException("Password not strong enough", 422)
    elif any(map(" ".__gt__, json["new"])):
        # control character
        raise HTTPException("Invalid character in password", 422)

    # check current password is correct
    hashed_current = await connection().fetchval(
        "select password from users where id = $1", request.user.id
    )
    if not verify_password(hashed_current, json["current"]):
        raise HTTPException("Incorrect password", 401)

    # update password
    hashed_new = hash_password(json["new"])
    await connection().execute(
        "update users set password = $1 where id = $2", hashed_new, request.user.id
    )
    return ORJSONResponse()


routes = [
    change_password,
    patch_account_email,
    patch_account_name,
    delete_account,
    get_account,
]
