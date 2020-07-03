import os
from email.mime.multipart import MIMEMultipart
from unittest.mock import MagicMock

import pytest

pytestmark = pytest.mark.asyncio


def async_(f):
    async def inner(*args, **kwargs):
        return f(*args, **kwargs)

    return inner


async def test_email(monkeypatch):
    import tome.email
    import tome.settings

    with open("templates/email/test.txt", "w") as f:
        f.write(
            """This is a generic template used to test email template rendering.
        Foo + Bar = {{ foo + bar }}
        """
        )

    monkeypatch.setattr(tome.settings, "SMTP_ENABLED", True)

    mime_multipart = MagicMock(spec=MIMEMultipart)
    mime_multipart.return_value = mime_multipart
    send_message = MagicMock()
    monkeypatch.setattr(tome.email.smtp, "send_message", async_(send_message))
    monkeypatch.setattr(tome.email, "MIMEMultipart", mime_multipart)

    await tome.email.send_message(
        "foo@example.com", "subject", "test", foo=2, bar=5
    )
    send_message.assert_called_with(mime_multipart)

    os.remove("templates/email/test.txt")
