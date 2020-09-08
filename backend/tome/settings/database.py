from tome.settings.core import get

# password, user, database name, port, host
POSTGRES_PASSWORD = get("POSTGRES_PASSWORD", ..., "")
POSTGRES_USER = get("POSTGRES_USER", "tome", "")
POSTGRES_DB = get("POSTGRES_DB", POSTGRES_USER, "")
POSTGRES_PORT = int(get("POSTGRES_PORT", "5432", ""))
POSTGRES_HOST = get("POSTGRES_HOST", "db", "")
