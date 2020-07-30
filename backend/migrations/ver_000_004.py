"""add basic node table"""

import asyncpg  # type: ignore


async def upgrade(conn: asyncpg.Connection) -> None:
    """perform some queries to upgrade the database

    when creating extensions, use "create extension if not exists foo_ext" """
    await conn.execute(
        """
        create table nodes (
        id uuid primary key default uuid_generate_v4(),
        content text not null default '',
        user_id uuid not null references users (id),
        parent uuid references nodes (id)
        );
        """
    )


async def downgrade(conn: asyncpg.Connection) -> None:
    """perform some queries to downgrade the database

    do not drop extensions here!"""
    await conn.execute("drop table nodes;")
