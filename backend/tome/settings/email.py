from .core import _bool, _get

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
