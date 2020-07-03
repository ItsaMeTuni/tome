"""tome migrations command-line runner"""

import argparse
import asyncio
import logging
import sys

import migrations

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

try:
    exit_code = asyncio.run(migrations.main(whither=args.whither, dry_run=args.dry_run))
except KeyboardInterrupt:
    logger.error("keyboard interrupt: rolled back")
    exit_code = 130
except BaseException as e:
    logger.critical("a fatal error occurred", exc_info=e)
    raise

sys.exit(exit_code)
