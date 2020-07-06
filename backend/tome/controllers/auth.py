import time
from datetime import datetime
from typing import List, Optional, Sequence, Tuple, cast
from uuid import UUID

import jwt
import orjson

from tome.database import connection
from tome.exceptions import HTTPException
from tome.models.user import User
from tome.settings import ALGORITHM, AUDIENCE, EXPIRY, ISSUER, SECRET_KEY
from tome.utils import ORJSONCodec

ALLOWED_API_KEY_SCOPES: frozenset = frozenset(())


async def get_auth_token(user: User, scope: List[str]) -> str:
    now = time.time()
    return jwt.encode(
        {
            "sub": user.id,
            "iat": now,
            "nbf": now,
            "exp": now + EXPIRY,
            "iss": ISSUER,
            "aud": AUDIENCE,
            "scope": scope,
        },
        algorithm=ALGORITHM,
        key=SECRET_KEY,
        json_encoder=ORJSONCodec,
    ).decode()


async def validate_auth_token(token: bytes) -> Tuple[User, List[str]]:
    try:
        payload = jwt.decode(
            token,
            algorithms=[ALGORITHM],
            key=SECRET_KEY,
            issuer=ISSUER,
            audience=AUDIENCE,
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException("invalid token", 401) from e
    user = await connection().fetchrow(
        "SELECT id, name, email FROM users WHERE id = $1", payload["sub"]
    )
    if user is None:
        raise HTTPException("account not available", 409)
    return User(**user), payload["scope"]


async def validate_api_key(uuid: UUID) -> Tuple[User, List[str]]:
    result = await connection().fetchrow(
        "select api_keys.scope, users.id, users.name, users.email, api_keys.expiry "
        "from api_keys inner join users on api_keys.user_id = users.id "
        "where api_keys.id = $1 limit 1",
        uuid,
    )
    if result is None:
        raise HTTPException("invalid API key", 401)
    if result["expiry"] is not None and result["expiry"] <= datetime.now():
        # expired
        raise HTTPException("invalid API key", 401)
    return (
        User(name=result["name"], email=result["email"], id=result["id"]),
        orjson.loads(result["scope"]),
    )


async def create_api_key(
    expiry: Optional[datetime], user: User, scope: Sequence[str]
) -> UUID:
    if set(scope) - ALLOWED_API_KEY_SCOPES:
        raise HTTPException("cannot issue an API token with this scope", 422)
    key = await connection().fetchval(
        "insert into api_keys (scope, user_id, expiry) values ($1, $2, $3) returning id",
        orjson.dumps(scope).decode(),
        user.id,
        expiry,
    )
    return cast(UUID, key)