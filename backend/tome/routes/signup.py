from uuid import UUID

import asyncpg  # type: ignore
import email_validator  # type: ignore
from starlette.requests import Request

from tome import settings
from tome.controllers.auth import decode_jwt
from tome.controllers.password import check_password_strength, hash_password
from tome.database import connection
from tome.email import send_message
from tome.exceptions import HTTPException
from tome.middleware.auth import requires
from tome.responses import ORJSONResponse
from tome.routing import get, post
from tome.utils import get_json, validate_types_raising


async def _create_account(name: str, email: str, password: str) -> UUID:
    if not name:
        raise HTTPException("empty name", 422)
    check_password_strength(password)
    try:
        return await connection().fetchval(
            """
            insert into users (email, name, password) values ($1, $2, $3) returning id;
            """,
            email,
            name,
            hash_password(password),
        )
    except asyncpg.UniqueViolationError as e:
        raise HTTPException("email address in use", 422) from e


@get("/api/signup")
async def check_signup_availability(_request: Request) -> ORJSONResponse:
    return ORJSONResponse(
        {
            "enabled": settings.SIGNUP_ENABLED,
            "email_confirm_required": settings.SIGNUP_EMAIL_CONFIRM_REQUIRED,
        }
    )


@post("/api/signup")
@requires("anonymous")
async def signup_no_confirm(request: Request) -> ORJSONResponse:
    json = await get_json(request)
    validate_types_raising(json, {"name": str, "password": str, "email": str})
    try:
        email_validator.validate_email(json["email"])
    except email_validator.EmailNotValidError as e:
        raise HTTPException("invalid email address", 422) from e

    user_id = await _create_account(**json)

    return ORJSONResponse(user_id, 201)


@post("/api/signup")
@requires("anonymous")
async def signup(request: Request) -> ORJSONResponse:
    json = await get_json(request)
    validate_types_raising(json, str)
    try:
        email = email_validator.validate_email(json)
    except email_validator.EmailNotValidError as e:
        raise HTTPException("invalid email address", 422) from e

    if await connection().fetchval("""select id from users where email = $1""", email):
        raise HTTPException("email address in use", 422)

    await send_message(email, "Confirm Tome account", "signup_confirm")
    return ORJSONResponse(None, 202)


@post("/api/signup/confirm")
async def signup_confirm(request: Request) -> ORJSONResponse:
    json = await get_json(request)
    validate_types_raising(json, {"name": str, "password": str, "token": str})

    email = decode_jwt(json["token"])["sub"]
    json["email"] = email

    try:
        user_id = await _create_account(**json)
    except HTTPException as e:
        raise HTTPException("account has already been created", 409) from e

    return ORJSONResponse(user_id, 201)


routes = [check_signup_availability]

if settings.SIGNUP_ENABLED:
    if settings.SIGNUP_EMAIL_CONFIRM_REQUIRED:
        routes += [signup, signup_confirm]
    else:
        routes += [signup_no_confirm]
