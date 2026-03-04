# Garmin Data Project

## Garmin Connect CLI

To access Garmin Connect data, use the CLI at `garmin_cli.py`. Run with `uv run garmin_cli.py`.

Read the module docstring at the top of `garmin_cli.py` for all available commands, flags, and examples.

Auth requires two env vars: `GARMIN_COOKIE` and `GARMIN_CSRF_TOKEN` (extracted from browser dev tools on connect.garmin.com).

## API Spec

Full API documentation is in `garmin-api-spec.md`. Reference this when adding new endpoints to the CLI.
