# Garmin Connect CLI

A command-line tool for accessing Garmin Connect APIs. Outputs raw JSON for programmatic use.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests
```

## Authentication

Extract these two values from browser dev tools on [connect.garmin.com](https://connect.garmin.com):
- **Cookie**: the full `Cookie` header value
- **CSRF Token**: the `Connect-Csrf-Token` header value

Set them as environment variables:

```bash
export GARMIN_COOKIE='your_cookie_value'
export GARMIN_CSRF_TOKEN='your_csrf_token_value'
```

Or pass them as CLI flags: `--cookie '...' --csrf-token '...'`

## Usage

```bash
python garmin_cli.py --help
python garmin_cli.py activities search --limit 20 --start 0 --activity-type running
python garmin_cli.py sleep stats --start-date 2026-02-21 --end-date 2026-02-27
```

See the module docstring in `garmin_cli.py` for all available commands, flags, and examples.
