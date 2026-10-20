"""
This package sends emails using SMTP. It supports attachments, CC, and BCC.
"""
import os
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from .env import ENV


def send_email(
    recipients: list,
    subject: str = '',
    body: str = '',
    files: list = None,
    cc: list = None,
    bcc: list = None,
) -> None:
    """
    Send an email with optional attachments, CC, and BCC.
    Emails may be a list or ; separated string.
    """

    cc = cc or []
    bcc = bcc or []

    # Combine all recipients for SMTP delivery
    all_recipients = recipients + cc + bcc

    smtp_object = _get_smtp_conn()

    msg = MIMEMultipart()
    msg['From'] = ENV['address']
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject

    if cc:
        msg['Cc'] = ', '.join(cc)

    # Do NOT add a Bcc header.
    # BCC recipients remain hidden from other recipients.

    msg.attach(MIMEText(body, 'plain'))

    if files:
        for file in files:
            part = MIMEBase('application', 'octet-stream')

            with open(file, 'rb') as attachment:
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            file_name = os.path.basename(file)

            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{file_name}"',
            )
            msg.attach(part)

    try:
        smtp_object.send_message(
            msg,
            to_addrs=all_recipients,
        )
        print(
            f'Email sent to {recipients}, CC: {cc}, '
            f'BCC: {len(bcc)} recipient(s), subject "{subject}"'
        )
    finally:
        smtp_object.quit()


def _get_smtp_conn() -> SMTP:
    smtp_object = SMTP(ENV['host'])
    smtp_object.connect(
        host=ENV['host'],
        port=int(ENV['port'])
    )
    smtp_object.starttls()
    smtp_object.login(
        user=ENV['address'],
        password=ENV['password']
    )
    return smtp_object

