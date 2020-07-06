"""create users table"""

import asyncpg  # type: ignore


async def upgrade(conn: asyncpg.Connection) -> None:
    """perform some queries to upgrade the database

    when creating extensions, use "create extension if not exists foo_ext" """
    await conn.execute(
        """
        create extension if not exists "uuid-ossp";
        create table users (
            id uuid primary key default uuid_generate_v4(),
            email text unique not null,
            name text not null,
            password text not null
        );"""
    )


async def downgrade(conn: asyncpg.Connection) -> None:
    """perform some queries to downgrade the database

    do not drop extensions here!"""
    ...
