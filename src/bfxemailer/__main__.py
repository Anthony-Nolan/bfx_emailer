"""
Argparse for the command line interface
of the application.
"""
import argparse
from . import send_email

def parse_args() -> None:
    parser = argparse.ArgumentParser(
        description='Send an email with optional attachment.'
    )
    parser.add_argument(
        '-r', '--recipients',
        type=str,
        required=True,
        nargs='+',
        help='Email addresses to send to'
    )
    parser.add_argument(
        '--cc',
        type=str,
        default=None,
        nargs='+',
        help='Email addresses to CC'
    )
    parser.add_argument(
        '--bcc',
        type=str,
        default=None,
        nargs='+',
        help='Email addresses to BCC'
    )
    parser.add_argument(
        '-s', '--subject',
        type=str,
        required=True,
        help='Subject of the email'
    )
    parser.add_argument(
        '-b', '--body',
        type=str,
        default='',
        help='Body of the email'
    )
    parser.add_argument(
        '-f', '--files',
        type=str,
        default=None,
        nargs='+',
        help='Files to attach to the email'
    )

    args = parser.parse_args()

    send_email(
        recipients=args.recipients,
        subject=args.subject,
        body=args.body,
        files=args.files,
        cc=args.cc,
        bcc=args.bcc
    )

def main() -> None:
    parse_args()

if __name__ == '__main__':
    main()

