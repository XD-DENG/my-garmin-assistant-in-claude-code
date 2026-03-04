# Garmin Connect CLI

A command-line tool for accessing Garmin Connect APIs. Outputs raw JSON for programmatic use.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests brotli requests-oauthlib
```

## Authentication

### Recommended: OAuth login (no browser dev tools needed)

Log in with your Garmin email and password:

```bash
python garmin_auth.py
```

Tokens are saved to `~/.garmin_tokens/`. The OAuth1 token lasts ~1 year; OAuth2 tokens refresh automatically. The CLI reads tokens automatically — no env vars or flags needed.

### Alternative: Manual cookie auth

Extract Cookie + CSRF token from browser dev tools on [connect.garmin.com](https://connect.garmin.com) and provide them via env vars or CLI flags:

```bash
export GARMIN_COOKIE='your_cookie_value'
export GARMIN_CSRF_TOKEN='your_csrf_token_value'
```

Auth priority: CLI flags > env vars > `~/.garmin_tokens/` (OAuth).

## Usage

```bash
python garmin_cli.py --help
python garmin_cli.py activities search --limit 20 --start 0 --activity-type running
python garmin_cli.py activities download --activity-id 22048373565
python garmin_cli.py sleep stats --start-date 2026-02-21 --end-date 2026-02-27
```

See the module docstring in `garmin_cli.py` for all available commands, flags, and examples.

## API Reference

- **`garmin-api-spec.md`** — Primary API documentation (activities, sleep, scores, calendar, FIT file download). Covers the endpoints currently implemented in the CLI plus the activity file download API.
- **`garmin-api-from-garth.md`** — Supplementary endpoints extracted from the [garth](https://github.com/matin/garth) Python package. Covers wellness/health data (heart rate, HRV, stress, body battery, steps, weight, hydration, intensity minutes, training readiness/status, user profile/settings) not yet in the primary spec.
