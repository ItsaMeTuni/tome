from .core import as_bool, get
from . import email

__all__ = ["SIGNUP_ENABLED", "SIGNUP_EMAIL_CONFIRM_REQUIRED"]

SIGNUP_ENABLED = as_bool(get("SIGNUP_ENABLED", True))
SIGNUP_EMAIL_CONFIRM_REQUIRED = as_bool(
    get("SIGNUP_EMAIL_CONFIRM_REQUIRED", email.SMTP_ENABLED)
)
