import base64
import io
import urllib.parse

import email_validator  # type: ignore
import pyotp  # type: ignore
from qrcode import make as make_qr_code  # type: ignore
from qrcode.image.svg import SvgPathFillImage  # type: ignore
from starlette.requests import Request

from tome.controllers.password import (
    check_password_strength,
    hash_password,
    verify_password,
)
from tome.database import connection
from tome.exceptions import HTTPException
from tome.middleware.auth import requires
from tome.responses import ORJSONResponse
from tome.routing import delete, get, patch, post
from tome.utils import get_json, validate_types_raising

TOTP_ISSUER = "Tome"


@get("/api/me")
@requires("account.read")
async def get_account(request: Request) -> ORJSONResponse:
    return ORJSONResponse(
        {"id": request.user.id, "email": request.user.email, "name": request.user.name,}
    )


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


@post("/api/me/password")
@requires("account.password")
async def change_password(request: Request) -> ORJSONResponse:
    json = await get_json(request)
    validate_types_raising(json, {"new": str, "current": str})

    # check new password validity
    if json["new"] == json["current"]:
        # same as current (even if current is incorrect, we needn't bother checking)
        raise HTTPException("Password not changed", 422)
    check_password_strength(json["new"])

    # check current password is correct
    if not verify_password(request.user.password, json["current"]):
        raise HTTPException("Incorrect password", 401)

    # update password
    hashed_new = hash_password(json["new"])
    await connection().execute(
        "update users set password = $1 where id = $2", hashed_new, request.user.id
    )
    return ORJSONResponse()


"""
                Explanation of two-factor state in database

                             <             Secret value            >
                             
                             +---------------+---------------------+
                             |      null     |       not null      |
            +----------------+---------------+---------------------+
      A     |      null      |    disabled   |  setup in progress  |
  recovery  +----------------+---------------+---------------------+
    value   |    not null    |  impossible™  |   setup complete    |
      v     +----------------+---------------+---------------------+

"""


@get("/api/me/two_factor")
@requires("account.two_factor")
async def get_two_factor_status(request: Request) -> ORJSONResponse:
    if request.user.two_factor_recovery:
        two_factor_status = "setup_complete"
    elif request.user.two_factor_secret:
        two_factor_status = "setup_in_progress"
    else:
        two_factor_status = "disabled"
    return ORJSONResponse(
        {"status": two_factor_status, "recovery": request.user.two_factor_recovery}
    )


@post("/api/me/two_factor/begin_setup")
@requires("account.two_factor")
async def begin_two_factor_setup(request: Request) -> ORJSONResponse:
    if request.user.two_factor_recovery:
        raise HTTPException("Already enabled", 422)
    elif request.user.two_factor_secret:
        raise HTTPException("Setup already started", 422)

    secret = pyotp.random_base32(32)

    await connection().execute(
        "update users set two_factor_secret = $1 where id = $2", secret, request.user.id
    )

    return ORJSONResponse(
        {"secret": secret, "qr_code_url": make_totp_qr_code(secret, request.user.email)}
    )


@post("/api/me/two_factor/confirm_setup")
@requires("account.two_factor")
async def confirm_two_factor_setup(request: Request) -> ORJSONResponse:
    json = await get_json(request)
    validate_types_raising(json, str)

    if request.user.two_factor_recovery:
        raise HTTPException("Already confirmed", 422)
    if not request.user.two_factor_secret:
        raise HTTPException("Not enabled", 422)
    if not pyotp.TOTP(request.user.two_factor_secret).verify(json):
        raise HTTPException("Incorrect code", 422)

    recovery = pyotp.random_base32(32)
    await connection().execute(
        "update users set two_factor_recovery = $1 where id = $2",
        recovery,
        request.user.id,
    )
    return ORJSONResponse(recovery)


@post("/api/me/two_factor/cancel_setup")
@requires("account.two_factor")
async def cancel_two_factor_setup(request: Request) -> ORJSONResponse:
    if not request.user.two_factor_secret:
        raise HTTPException("Not enabled", 422)
    if request.user.two_factor_recovery:
        raise HTTPException("Already confirmed", 422)
    await connection().execute(
        "update users set two_factor_secret = null where id = $1", request.user.id
    )
    return ORJSONResponse()


@delete("/api/me/two_factor")
@requires("account.two_factor")
async def disable_two_factor(request: Request) -> ORJSONResponse:
    await connection().execute(
        """
        update users set
            two_factor_secret = null,
            two_factor_recovery = null
        where id = $1
        """,
        request.user.id,
    )
    return ORJSONResponse()


@post("/api/auth/two_factor/reset_recovery")
@requires("account.two_factor")
async def reset_two_factor_recovery_code(request: Request) -> ORJSONResponse:
    recovery = pyotp.random_base32(32)
    await connection().execute(
        """
        update users set two_factor_recovery = $1 where id = $2
        """,
        recovery,
        request.user.id,
    )
    return ORJSONResponse(recovery)


def make_totp_qr_code(secret: str, email: str) -> str:
    account_label = urllib.parse.quote(email.replace(":", "_"))
    totp_uri = (
        f"otpauth://totp/{TOTP_ISSUER}:{account_label}"
        f"?issuer={TOTP_ISSUER}&secret={secret}"
    )
    qr_code = make_qr_code(totp_uri, image_factory=SvgPathFillImage)
    buffer = io.BytesIO()
    qr_code.save(buffer)
    encoded_qr_code = base64.b64encode(buffer.getvalue()).decode()
    return "data:image/svg+xml;base64," + encoded_qr_code


routes = [
    change_password,
    patch_account_email,
    patch_account_name,
    delete_account,
    get_account,
    get_two_factor_status,
    begin_two_factor_setup,
    confirm_two_factor_setup,
    cancel_two_factor_setup,
    disable_two_factor,
    reset_two_factor_recovery_code,
]
