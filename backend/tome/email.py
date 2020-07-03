from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

import aiosmtplib  # type: ignore
import jinja2

from tome import settings

templates = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates/email"),
    autoescape=False,
    enable_async=True,
)

smtp = aiosmtplib.SMTP(
    hostname=settings.SMTP_HOSTNAME,
    port=settings.SMTP_PORT,
    username=settings.SMTP_USERNAME,
    password=settings.SMTP_PASSWORD,
    use_tls=settings.SMTP_DIRECT_TLS,
    start_tls=settings.SMTP_START_TLS,
)


async def connect() -> None:
    (
        settings.SMTP_ENABLED
        and await smtp.connect()
        or settings.SMTP_ENABLED
        and settings.SMTP_START_TLS
        and await smtp.starttls()
    )


async def disconnect() -> None:
    # noinspection PyStatementEffect
    smtp.is_connected and await smtp.quit()


async def send_message(
    to: str, subject: str, template_name: str, /, **values: Any
) -> None:
    if settings.SMTP_ENABLED:
        message = MIMEMultipart()
        message["From"] = settings.SMTP_FROM
        message["To"] = to
        message["Subject"] = subject
        template = templates.get_template(template_name + ".txt")
        message.attach(
            MIMEText(await template.render_async(**values), "plain", "utf-8")
        )
        await smtp.send_message(message)
