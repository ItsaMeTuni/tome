"""this is a template file for migration versions"""

import asyncpg  # type: ignore


async def upgrade(conn: asyncpg.Connection) -> None:
    """perform some queries to upgrade the database

    when creating extensions, use "create extension if not exists foo_ext" """
    ...


async def downgrade(conn: asyncpg.Connection) -> None:
    """perform some queries to downgrade the database

    do not drop extensions here!"""
    ...
