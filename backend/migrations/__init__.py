"""simple python migration system for asyncpg"""

import importlib.util
import logging
import os
import pathlib
from types import ModuleType
from typing import Generator, List, Optional, Tuple, cast

import asyncpg  # type: ignore

logger = logging.getLogger("tome.migrations")


async def init_migrations_table(conn: asyncpg.Connection) -> None:
    """create the migrations table and its value"""
    async with conn.transaction():
        await conn.execute(
            "create table if not exists migration_version ("
            "   the boolean not null primary key default true,"
            "   constraint the check (the),"
            "   id varchar default null);"
            "insert into migration_version default values on conflict do nothing;"
        )


def get_versions() -> Generator[Tuple[str, ModuleType], None, None]:
    """find all available version modules and return them, in tuples of (id, module)"""
    logger.debug("discovering versions...")
    files = sorted(pathlib.Path(__file__).parent.glob("ver_*.py"))
    for version in files:
        name = version.name[:-3]
        if not name.isidentifier():
            # not a valid module name
            logging.debug(f"ignoring invalid version ID at {version}")
            continue
        # import the module here because it reduces race conditions
        logging.debug(f"found version at {version}")
        yield name, importlib.import_module("migrations." + name)


async def get_current_version(conn: asyncpg.Connection) -> Optional[str]:
    """fetch the current migration version from the database"""
    return cast(
        Optional[str],
        (await conn.fetchrow("""select id from migration_version limit 1"""))[0],
    )


async def update_current_version(conn: asyncpg.Connection, version: str) -> None:
    """update the stored current version in the database"""
    await conn.execute("""update migration_version set id = $1 where the""", version)


async def main(whither: Optional[str] = None, *, dry_run: bool = False) -> int:
    """main method, discovers and runs specified migrations

    whither: version id to upgrade/downgrade to. if None, use the latest available
    dry_run: print the migrations that would be run instead of actually executing them

    return: status code (0 = success, >1 otherwise)
    """
    versions = list(get_versions())

    if whither and whither not in dict(versions):
        logger.critical(f"could not find the specified version: {whither}")
        return 1

    dsn = os.getenv("TOME_DSN")
    if not dsn:
        logger.critical(
            "please set the $TOME_DSN environment variable"
            " to a 'postgresql://user:pass@server:port/db' URI"
        )
        return 1

    conn = await asyncpg.connect(dsn)
    try:
        return await migrate(
            conn=conn, versions=versions, whither=whither, dry_run=dry_run
        )
    finally:
        await conn.close()


async def migrate(
    *,
    conn: asyncpg.Connection,
    versions: List[Tuple[str, ModuleType]],
    whither: Optional[str] = None,
    dry_run: bool = False,
) -> int:
    """executes the migrations in `versions`"""
    logger.info("initialising")
    try:
        await init_migrations_table(conn)
    except Exception as e:
        logger.critical("failed to initialise migrations table", exc_info=e)
        return 2

    current: Optional[str] = await get_current_version(conn)
    logger.debug(f"current version: {current}")

    current_index: int = -1
    whither_index: int = len(versions) - 1
    for i, (k, _) in enumerate(versions):
        if k == current:
            current_index = i
        if k == whither:
            whither_index = i

    logger.debug(f"whither at index {whither_index}")
    logger.debug(f"current at index {current_index}")

    try:
        async with conn.transaction():
            total: int = abs(current_index - whither_index)

            if whither_index > current_index:
                text = "==> Upgrading"
                attr = "upgrade"
                step = 1
            elif current_index > whither_index:
                text = "<== Downgrading"
                attr = "downgrade"
                step = -1
            else:
                logger.warning("=== Nothing to do")
                return 0

            logger.info(f"{text} from {current} to {whither} ({total} steps)")
            start = current_index + step
            end = whither_index + step

            for i, (version, module) in enumerate(versions[start:end:step]):
                logger.info(f"{text} with ver_{version}.py ({i+1}/{total})")
                if dry_run:
                    continue

                try:
                    async with conn.transaction():
                        fn = getattr(module, attr)
                        logger.debug(f"executing migration {fn}")
                        await fn(conn)
                        logger.debug("updating current version in database")
                        await update_current_version(conn, version)
                except Exception as e:
                    logger.error(
                        f"failed while executing migration {version}", exc_info=e
                    )
                    raise
    except Exception as e:
        logger.debug("exception info", exc_info=e)
        logger.critical("a.critical error occurred")
        return 2
    else:
        return 0
