"""tome migrations command-line runner"""

import argparse
import asyncio
import logging
import sys

import migrations
import tome.database

LOG_LEVELS = {
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

logger = logging.getLogger("tome.migrations")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--dry-run",
    "-d",
    help="print the migrations that would be run instead of actually executing them",
    action="store_true",
)
parser.add_argument(
    "--log-level", help="configure the log level", choices=LOG_LEVELS, default="info"
)
parser.add_argument(
    "whither",
    nargs="?",
    default=None,
    help="version to upgrade or downgrade to (default: latest)",
)

args = parser.parse_args()

logger.setLevel(LOG_LEVELS[args.log_level])


async def main() -> int:
    """main async portion of command-line runner. returns status code 0-255"""
    try:
        await tome.database.connect()
        return await migrations.main(
            whither=args.whither,
            conn=tome.database.connection(),
            dry_run=args.dry_run
        )
    except KeyboardInterrupt:
        logger.critical("keyboard interrupt")
        try:
            await tome.database.disconnect()
        except Exception as e:
            logger.error("failed to cleanly disconnect database", exc_info=e)
        logger.info("rolled back")
        return 130
    except Exception as e:
        logger.critical("a fatal error occurred!", exc_info=e)
        await tome.database.disconnect()
        logger.info("rolled back")
        return 3
    finally:
        await tome.database.disconnect()


sys.exit(asyncio.run(main()) or 0)
