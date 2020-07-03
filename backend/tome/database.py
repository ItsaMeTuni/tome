import asyncpg  # type: ignore

from tome import settings

_connection: asyncpg.Connection = None


def connection() -> asyncpg.Connection:
    return _connection


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


async def disconnect() -> None:
    global _connection
    if connection:
        await _connection.close()
        _connection = None
