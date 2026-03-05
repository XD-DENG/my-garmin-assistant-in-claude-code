# Garmin Data Project

## Python executable
When need to run `python` at any time, follow the steps below:
1. check if `venv` directory presents in the workspace, if yes, run `source venv/bin/activate`, then use `python` directly
2. if `venv` directory doesn't exist, follow the instructions in README.md to create a venv and install dependencies, then try step 1 again
3. if `venv` directory exist, but step 1 still fails in the end, remove `venv` directory and then follow the instructions in README.md to create a venv and install dependencies, then try step 1 again
4. if step 1/2/3 all don't work, find another way to find a usable Python executable.

## Garmin Connect CLI

To access Garmin Connect data, use the CLI at `garmin_cli.py`. Run with `python garmin_cli.py` (using the venv described in README.md). If needed to install dependencies, follow the instructions in README.md.

Read the module docstring at the top of `garmin_cli.py` for all available commands, flags, and examples.

### Authentication

Auth priority: CLI flags > env vars > `~/.garmin_tokens/` (OAuth).

**Preferred method — OAuth login:**
1. Run `python garmin_auth.py` — prompts for Garmin email + password
2. Tokens are saved to `~/.garmin_tokens/` (OAuth1 lasts ~1 year, OAuth2 auto-refreshes)
3. The CLI reads tokens automatically — no flags or env vars needed
4. Re-run `python garmin_auth.py` if the OAuth1 token eventually expires (~1 year)

When the user gets auth errors, tell them to re-run `python garmin_auth.py`.

**Fallback method — manual cookie auth:**
If the user prefers, they can provide credentials via env vars (`GARMIN_COOKIE`, `GARMIN_CSRF_TOKEN`) or CLI flags (`--cookie`, `--csrf-token`). Ask the user to paste the curl command from browser dev tools, then parse the cookie and token from it.

**Cookie shell escaping** (only relevant for cookie auth): The Garmin cookie contains `|`, `*`, `~`, and other characters that break shell variable expansion. Write the cookie to a temp file using a Bash heredoc (`cat > /tmp/garmin_cookie.txt << 'EOF'`), then pass it to the CLI via `--cookie "$(cat /tmp/garmin_cookie.txt)"`. Do NOT paste the cookie directly into a shell `export` command or use the Write tool (which may fail if the file hasn't been read first).

### CLI Gotchas

- **`--start 0` is required for `activities search`** — it's easy to forget but the command will fail without it. Always include `--start 0` (or another offset) alongside `--limit`.

- **Global flags (`--output`, `--cookie`, `--csrf-token`) must appear BEFORE the subcommand**. This is an argparse limitation. Example: `python garmin_cli.py --output file.json activities search --limit 5 --start 0` (correct) vs `... activities search --limit 5 --output file.json` (wrong — argparse error).

- **Activity type filtering uses two flags**: `--activity-type` for parent types (e.g. `running`, `racket_sports`, `winter_sports`, `fitness_equipment`) and `--activity-sub-type` for sub-types (e.g. `trail_running`, `tennis_v2`, `resort_skiing_snowboarding_ws`). Use `--activity-type` alone to get all activities in a category, or add `--activity-sub-type` to narrow down. `--activity-sub-type` requires `--activity-type`.

- **Sub-type keys are non-obvious** — they often don't match the common activity name (e.g. `tennis_v2` not `tennis`, `resort_skiing_snowboarding_ws` not `skiing`). When unsure of the key, use `--search` first and inspect `activityType.typeKey` in the response to discover the actual key. Note: `--search` does free-text matching on activity names, so results may include false positives — filter by `activityType.typeKey` to get exact matches.

- **Parent/sub-type naming overlap** — some parent type keys are reused as sub-type `typeKey` values in response data. For example, `running` is both the parent type and the `typeKey` for road/generic runs. When the user says "running", they typically mean **all running** (the parent), not just the `running` sub-type. When breaking down sub-types, label the `running` typeKey as "road/generic running" to avoid ambiguity.

### Downloading FIT Files

To download the raw FIT file for an activity (API 9: download-service):

```bash
# Download FIT file (extracts from ZIP automatically)
python garmin_cli.py activities download --activity-id 22048373565

# Download to a specific directory
python garmin_cli.py activities download --activity-id 22048373565 --output-dir /tmp
```

The FIT file is saved as `{activityId}_ACTIVITY.fit`. To get the activity ID, use `python garmin_cli.py activities search` first and read the `activityId` field from the results.

To parse the FIT file, use `fitdecode` (`pip install fitdecode`). See API 9 in `garmin-api-spec.md` for details on the FIT format and what data it contains (GPS trackpoints, per-second HR/cadence/power, laps, etc.).

### Activity Gear

To get gear (shoes, bike, etc.) linked to an activity (API 10: gear-service):

```bash
python garmin_cli.py activities gear --activity-id 21993647638
```

Returns an array of gear objects with brand, usage stats (distance, duration, days used), and retirement threshold (`maxUsageDistanceMeters`). Returns an empty array if no gear is linked. Useful for tracking shoe mileage or equipment wear.

## API Spec

Full API documentation is in `garmin-api-spec.md`. Reference this when adding new endpoints to the CLI.

If the user requests data not covered by `garmin-api-spec.md` (e.g. heart rate time-series, HRV, stress, body battery, steps, weight, hydration, intensity minutes, training readiness/status, user profile/settings), check `garmin-api-from-garth.md` for additional endpoints. These were extracted from the [garth](https://github.com/matin/garth) Python package and cover many wellness/health APIs that the primary spec does not.
