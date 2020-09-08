# secret key to sign auth tokens with
import secrets

from tome.settings.core import get

SECRET_KEY = get("JWT_SECRET_KEY", "") or secrets.token_urlsafe(32)
# audience and issuer for auth tokens
AUDIENCE = ISSUER = get("JWT_NAME", "tome")
# algorithm to sign auth tokens with
ALGORITHM = get("JWT_ALGORITHM", "HS256")
# expiry time in seconds for auth tokens
EXPIRY = int(get("JWT_EXPIRY", 86400))
