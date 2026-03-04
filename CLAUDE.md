# Garmin Data Project

## Garmin Connect CLI

To access Garmin Connect data, use the CLI at `garmin_cli.py`. Run with `python garmin_cli.py` (using the venv described in README.md). If needed to install dependencies, follow the instruciton in README.md.

Read the module docstring at the top of `garmin_cli.py` for all available commands, flags, and examples.

Auth requires two env vars: `GARMIN_COOKIE` and `GARMIN_CSRF_TOKEN` (extracted from browser dev tools on connect.garmin.com).

When needing the Cookie and Token, ask the user to paste the curl command from browser dev tools (in which cookie and token are available), then parse these info from the curl command for the user.

## API Spec

Full API documentation is in `garmin-api-spec.md`. Reference this when adding new endpoints to the CLI.
