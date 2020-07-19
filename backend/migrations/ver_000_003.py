"""add two-factor authentication support"""

import asyncpg  # type: ignore


async def upgrade(conn: asyncpg.Connection) -> None:
    """perform some queries to upgrade the database

    when creating extensions, use "create extension if not exists foo_ext" """
    await conn.execute(
        """
        alter table users
            add column two_factor_secret text,
            add column two_factor_recovery text;
        """
    )


async def downgrade(conn: asyncpg.Connection) -> None:
    """perform some queries to downgrade the database

    do not drop extensions here!"""
    await conn.execute(
        """
        alter table users
            drop column two_factor_secret,
            drop column two_factor_recovery;"""
    )
