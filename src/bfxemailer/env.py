"""
Loads environment variables for SMTP configuration
and validates their presence.
"""
import os

ENV = {
    'host': os.environ.get('SMTP_HOST', None),
    'port': (
        int(os.environ['SMTP_PORT']
        if os.environ.get('SMTP_PORT', None)
        else None
    )),
    'address': os.environ.get('SMTP_ADDRESS'),
    'password': os.environ.get('SMTP_PASSWORD')
}

for key, value in ENV.items():
    if not value:
        raise ValueError(f'Environment variable {key} is not set')


