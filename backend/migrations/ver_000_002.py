"""create API key table"""

import asyncpg  # type: ignore


async def upgrade(conn: asyncpg.Connection) -> None:
    """perform some queries to upgrade the database

    when creating extensions, use "create extension if not exists foo_ext" """
    await conn.execute(
        "create table api_keys ("
        "id uuid primary key default uuid_generate_v4(),"
        "scope jsonb not null,"
        "user_id uuid not null,"
        "expiry timestamp default null);"
    )


async def downgrade(conn: asyncpg.Connection) -> None:
    """perform some queries to downgrade the database

    do not drop extensions here!"""
    await conn.execute("drop table api_keys;")
