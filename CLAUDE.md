# Garmin Data Project

## Garmin Connect CLI

To access Garmin Connect data, use the CLI at `garmin_cli.py`. Run with `python garmin_cli.py` (using the venv described in README.md). If needed to install dependencies, follow the instruciton in README.md.

Read the module docstring at the top of `garmin_cli.py` for all available commands, flags, and examples.

### Authentication

Auth requires two env vars: `GARMIN_COOKIE` and `GARMIN_CSRF_TOKEN` (extracted from browser dev tools on connect.garmin.com).

When needing the Cookie and Token, ask the user to paste the curl command from browser dev tools (in which cookie and token are available), then parse these info from the curl command for the user.

**Cookie shell escaping**: The Garmin cookie contains `|`, `*`, `~`, and other characters that break shell variable expansion. Always pass credentials via env vars using `"$(cat file)"` or write a helper script — do NOT paste the cookie directly into a shell `export` command.

### CLI Gotchas

- **Global flags (`--output`, `--cookie`, `--csrf-token`) must appear BEFORE the subcommand**. This is an argparse limitation. Example: `uv run garmin_cli.py --output file.json activities search --limit 5 --start 0` (correct) vs `... activities search --limit 5 --output file.json` (wrong — argparse error).

- **`--activity-type` only accepts parent types** (e.g. `running`, `cycling`), NOT sub-types (e.g. `trail_running`, `pickleball`). The API returns error `"Activity type cannot be an activity sub type"`. To find sub-type activities, use `--search <name>` instead. Note: `--search` does free-text matching on activity names, so results may include false positives from other activity types that happen to contain the search term — filter by `activityType.typeKey` in the response to get exact matches.

## API Spec

Full API documentation is in `garmin-api-spec.md`. Reference this when adding new endpoints to the CLI.
