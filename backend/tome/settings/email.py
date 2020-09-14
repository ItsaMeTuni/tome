from .core import as_bool, get

# boolean, enable or disable sending emails
SMTP_ENABLED = as_bool(get("SMTP_ENABLED", "")) and ...
# hostname to connect to smtp
SMTP_HOSTNAME = get("SMTP_HOSTNAME", SMTP_ENABLED)
# port to connect to smtp
SMTP_PORT = int(get("SMTP_PORT", 25))
# username to login to smtp with
SMTP_USERNAME = get("SMTP_USERNAME", None)
# password to login to smtp with
SMTP_PASSWORD = get("SMTP_PASSWORD", None)
# enable direct TLS in smtp
SMTP_DIRECT_TLS = as_bool(get("SMTP_DIRECT_TLS", ""))
# enable starttls in smtp
SMTP_START_TLS = as_bool(get("SMTP_START_TLS", ""))
# email address to send emails from
EMAIL_FROM = get("EMAIL_FROM", SMTP_ENABLED)
