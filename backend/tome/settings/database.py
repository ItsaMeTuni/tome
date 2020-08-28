from tome.settings.core import _get

# password, user, database name, port, host
POSTGRES_PASSWORD = _get("POSTGRES_PASSWORD", ..., "")
POSTGRES_USER = _get("POSTGRES_USER", "tome", "")
POSTGRES_DB = _get("POSTGRES_DB", POSTGRES_USER, "")
POSTGRES_PORT = int(_get("POSTGRES_PORT", "5432", ""))
POSTGRES_HOST = _get("POSTGRES_HOST", "db", "")
