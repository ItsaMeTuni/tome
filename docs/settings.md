# Settings Reference

Settings are specified using environment variables to configure various integral
application settings. This page lists them.

Boolean values can be specified in the forms:
- `yes` or `no`
- `y` or `n`
- `true` or `false`
- `t` or `f`
- `1` or `0`

## Email
`TOME_SMTP_ENABLED`: (boolean) whether to enable sending emails (e.g. for password resets, security alerts, etc.). (Currently email sending is not implemented). Default false.

`TOME_SMTP_HOSTNAME`: (string) Hostname of the SMTP server to connect to. Required if SMTP is enabled.

`TOME_SMTP_PORT`: (integer) TCP Port number to connect to the SMTP server via. Default 25. If STARTTLS or direct TLS is enabled you'll probably want to set this to 587.

`TOME_SMTP_`: (string) Username with which to authenticate to the SMTP server. Will not login if not specified.

`TOME_SMTP_PASSWORD`: (string) Password with which to authenticate to the SMTP server.

`TOME_SMTP_`: (boolean) Enable the STARTTLS SMTP extension when connecting to the mail server. Default False.

`TOME_SMTP_DIRECT_TLS`: (boolean) Enable direct TLS connection to the SMTP server (sometimes called SMTPS). Default False.

`TOME_FROM_`: (string) SMTP FROM address to send emails using. To ensure your emails do not get marked as spam, make sure this is a domain the mail server is verified to send from (using SPF/DKIM). Required if SMTP is enabled.

## Database
**Note that these environment variables do not use the `TOME_` prefix as they are designed to be compatible with those used by the official [PostgreSQL Docker image](https://hub.docker.com/_/postgres)**

`POSTGRES_PASSWORD`: (string) Password with which to connect to the PostgreSQL database. Required.

`POSTGRES_USER`: (string) Username with which to connect to the PostgreSQL database. Default `tome`.

`POSTGRES_DB`: (string) PostgreSQL database name to connect to. Defaults to the same as the username.

`POSTGRES_PORT`: (integer) TCP Port to connect to the PostgreSQL database via.

`POSTGRES_HOST`: (string) Hostname of the PostgreSQL database server. Default `db`.


## JWT
`TOME_JWT_SECRET_KEY`: (string) a secret key used to sign and verify authentication tokens. If not supplied, a random one will be generated. (this means, however, that you will be logged out when the server restarts).

`TOME_JWT_ALGORITHM`: algorithm for signing and verifying authentication tokens. Default `HS256` (See RFC 12345§1.2.3 to choose the correct one). You don't need to change this.

`TOME_JWT_NAME`: (string) audience and issuer for authentication tokens. Default `tome`. You don't need to change this.

`TOME_JWT_EXPIRY`: (integer) time in seconds before authentication tokens expire. Default `86400` (one day).
