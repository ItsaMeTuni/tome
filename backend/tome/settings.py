import os
import secrets
from typing import Any

_PREFIX = "TOME_"


def _get(name: str, default: Any = ..., prefix: str = _PREFIX) -> Any:
    v = os.getenv(prefix + name.upper())
    if not v and default is ...:
        raise Exception(
            f"missing required environment variable {prefix + name.upper()}"
        )
    return v or default


def _bool(string: str) -> bool:
    return (
        string.lower().startswith("y")
        or string.lower().startswith("t")
        or string.lower().startswith("1")
    )


POSTGRES_PASSWORD = _get("POSTGRES_PASSWORD", ..., "")
POSTGRES_USER = _get("POSTGRES_USER", "tome", "")
POSTGRES_DB = _get("POSTGRES_DB", POSTGRES_USER, "")
POSTGRES_PORT = int(_get("POSTGRES_PORT", "5432", ""))
POSTGRES_HOST = _get("POSTGRES_HOST", "db", "")

# boolean, enable or disable sending emails
SMTP_ENABLED = _bool(_get("SMTP_ENABLED", "")) and ...
# hostname to connect to smtp
SMTP_HOSTNAME = _get("SMTP_HOSTNAME", SMTP_ENABLED)
# port to connect to smtp
SMTP_PORT = int(_get("SMTP_PORT", 25))
# username to login to smtp with
SMTP_USERNAME = _get("SMTP_USERNAME", None)
# password to login to smtp with
SMTP_PASSWORD = _get("SMTP_PASSWORD", None)
# enable direct TLS in smtp
SMTP_DIRECT_TLS = _bool(_get("SMTP_DIRECT_TLS", ""))
# enable starttls in smtp
SMTP_START_TLS = _bool(_get("SMTP_START_TLS", ""))
# email address to send emails from
SMTP_FROM = _get("SMTP_FROM", SMTP_ENABLED)

# secret key to sign auth tokens with
SECRET_KEY = _get("JWT_SECRET_KEY", "") or secrets.token_urlsafe(32)
# audience and issuer for auth tokens
AUDIENCE = ISSUER = _get("JWT_NAME", "tome")
# algorithm to sign auth tokens with
ALGORITHM = _get("JWT_ALGORITHM", "HS256")
# expiry time in seconds for auth tokens
EXPIRY = int(_get("JWT_EXPIRY", 86400))

DEBUG = _bool(_get("DEBUG", False))
