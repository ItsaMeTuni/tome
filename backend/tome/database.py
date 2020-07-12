import uuid
from typing import Any

import asyncpg  # type: ignore

from tome import settings

_connection: asyncpg.Connection = None


def connection() -> asyncpg.Connection:
    return _connection


def _uuid_coerce(value: Any) -> bytes:
    # TODO(pxeger) PEP 622
    if isinstance(value, str):
        return uuid.UUID(value).bytes
    elif isinstance(value, bytes):
        return value
    elif isinstance(value, uuid.UUID):
        return value.bytes
    elif isinstance(value, int):
        return uuid.UUID(int=value).bytes
    else:
        raise TypeError(f"cannot coerce object of type {type(value)} to a UUID")


async def connect() -> None:
    global _connection
    if not _connection or not _connection.is_closed():
        _connection = await asyncpg.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
        )
        await _connection.set_type_codec(
            "uuid",
            encoder=_uuid_coerce,
            decoder=lambda u: uuid.UUID(bytes=u),
            schema="pg_catalog",
            format="binary"
        )


async def disconnect() -> None:
    global _connection
    if connection:
        await _connection.close()
        _connection = None
