"""
Loads environment variables for SMTP configuration
and validates their presence.
"""
import os

ENV = {
    'host': os.environ.get('SMTP_HOST', None),
    'port': os.environ.get('SMTP_PORT', None),
    'address': os.environ.get('SMTP_ADDRESS'),
    'password': os.environ.get('SMTP_PASSWORD')
}

for key, value in ENV.items():
    if not value:
        raise ValueError(f'Environment variable SMTP_{key.upper()} is not set')

try:
    ENV['port'] = int(ENV['port'])
except ValueError:
    raise ValueError(
        f'Environment variable SMTP_PORT must be an integer, got {ENV["port"]!r}'
    ) from None


