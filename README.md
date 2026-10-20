# bfx_emailer

A lightweight wrapper for sending email over SMTP, both from the command line and programmatically from Python. It supports CC, BCC and file attachments, and uses only the Python standard library, so it has no third-party dependencies.

Requires a Python version newer than 3.6.

## Installation

### 1. Configure SMTP credentials

`bfx_emailer` reads its SMTP settings from four environment variables:

| Variable        | Description                                              |
| --------------- | -------------------------------------------------------- |
| `SMTP_HOST`     | SMTP server hostname, e.g. `smtp.office365.com`          |
| `SMTP_PORT`     | SMTP server port. Must support STARTTLS, e.g. `587`      |
| `SMTP_ADDRESS`  | Sender email address, also used as the SMTP login        |
| `SMTP_PASSWORD` | Password for the sender account                          |

All four must be set **before** you run the CLI or import the package. If any of them is missing, or `SMTP_PORT` isn't a number, the import raises a `ValueError` that names the variable.

Set them in one of two ways.

**Option A: copy and source the template file**

```bash
cp .env.blank .env
# Edit .env and fill in each value
source .env
```

`.env` is listed in `.gitignore`, so your credentials won't be committed.

**Option B: export the variables yourself**

```bash
export SMTP_HOST=smtp.example.com
export SMTP_PORT=587
export SMTP_ADDRESS=me@example.com
export SMTP_PASSWORD='your-password'
```

To keep the settings across sessions, add the `source` or `export` lines to your shell profile, for example `~/.bashrc`.

### 2. Install the package

From a local clone of the repository:

```bash
pip install .
```

Or install straight from GitHub without cloning:

```bash
# Over SSH (requires an SSH key registered with GitHub)
pip install "git+ssh://git@github.com/richardnatarajanAN/bfx_emailer.git"

# Over HTTPS
pip install "git+https://github.com/richardnatarajanAN/bfx_emailer.git"
```

Installing the package adds a `bfxemail` command to your environment.

## Usage

### Command line

```
bfxemail -r RECIPIENT [RECIPIENT ...] -s SUBJECT [-b BODY]
         [--cc CC [CC ...]] [--bcc BCC [BCC ...]]
         [-f FILE [FILE ...]]
```

| Option               | Required | Description                               |
| -------------------- | -------- | ----------------------------------------- |
| `-r`, `--recipients` | yes      | One or more recipient addresses           |
| `-s`, `--subject`    | yes      | Subject line                              |
| `-b`, `--body`       | no       | Plain-text body (empty by default)        |
| `--cc`               | no       | One or more CC addresses                  |
| `--bcc`              | no       | One or more BCC addresses                 |
| `-f`, `--files`      | no       | One or more file paths to attach          |

Separate multiple files with spaces. Separate multiple addresses with spaces or semicolons. Quote any argument that contains a semicolon, for example `-r "alice@example.com;bob@example.com"`.

Examples:

```bash
# Simple message
bfxemail -r richard@example.com -s "Pipeline results" -b "Something went wrong..."

# Several recipients, CC, BCC and attachments
bfxemail \
    -r tom@example.com jonny@example.com \
    --cc ig@example.com \
    --bcc bfx@example.com \
    -s "QC report" \
    -b "Good luck with the QC" \
    -f results/qc_report.html results/summary.tsv
```

You can also run the package as a module:

```bash
python -m bfxemailer -r alice@example.com -s "Hello"
```

### Python

Import `send_email` and call it:

```python
from bfxemailer import send_email

send_email(
    recipients=['alice@example.com', 'bob@example.com'],
    subject='QC report',
    body='Please find the QC report attached.',
    files=['results/qc_report.html', 'results/summary.tsv'],
    cc=['team@example.com'],
    bcc=['audit@example.com'],
)
```

| Parameter    | Type        | Default | Description                     |
| ------------ | ----------- | ------- | ------------------------------- |
| `recipients` | `list[str]` or `str` | —      | Recipient addresses (required)  |
| `subject`    | `str`                | `''`   | Subject line                    |
| `body`       | `str`                | `''`   | Plain-text body                 |
| `files`      | `list[str]`          | `None` | Paths of files to attach        |
| `cc`         | `list[str]` or `str` | `None` | CC addresses                    |
| `bcc`        | `list[str]` or `str` | `None` | BCC addresses                   |

Notes:

- Addresses can be a list or a `;`-separated string, so `'alice@example.com;bob@example.com'` is the same as `['alice@example.com', 'bob@example.com']`.
- If `recipients` is empty, the function raises a `ValueError`.
- BCC recipients receive the email, but no `Bcc` header is added, so other recipients can't see them.
- The SMTP environment variables are read when the module is imported, so set them before the `import`.
- On success, the function prints a short confirmation. On failure, it raises the underlying `smtplib` exception.
