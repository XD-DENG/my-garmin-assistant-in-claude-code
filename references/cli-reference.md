# Garmin Connect CLI — Complete Reference

## Overview

The CLI wraps 11 Garmin Connect APIs plus supplementary garth endpoints. It outputs raw JSON to stdout (or downloads binary files for FIT downloads). Designed for programmatic use (piping, scripting, LLM tool-use).

Run with:
```bash
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py <command>
```

## Global flags

**These must appear BEFORE the subcommand** (argparse limitation).

| Flag | Description |
|------|-------------|
| `--cookie TEXT` | Cookie header value (overrides `GARMIN_COOKIE` env var) |
| `--csrf-token TEXT` | CSRF token value (overrides `GARMIN_CSRF_TOKEN` env var) |
| `--output FILE` | Write JSON output to a file instead of stdout |

## Subcommands

### activities search

Search/filter activities (API 1: activitylist-service).

| Flag | Description |
|------|-------------|
| `--limit INT` | Max results to return (**required**) |
| `--start INT` | Pagination offset, 0-indexed (**required** — always include `--start 0`) |
| `--search TEXT` | Free-text search across activity names |
| `--activity-type TEXT` | Parent activity type key (e.g. `running`, `racket_sports`, `winter_sports`, `fitness_equipment`) |
| `--activity-sub-type TEXT` | Activity sub-type key (e.g. `trail_running`, `tennis_v2`, `resort_skiing_snowboarding_ws`). Requires `--activity-type`. |
| `--start-date DATE` | Filter start date, YYYY-MM-DD, inclusive |
| `--end-date DATE` | Filter end date, YYYY-MM-DD, inclusive |
| `--exclude-children` | Exclude child activities (multi-sport sub-activities) |

### activities detail

Get full detail for a single activity (API 2: activity-service).

| Flag | Description |
|------|-------------|
| `--activity-id INT` | Garmin activity ID (**required**) |

### activities download

Download original FIT file for an activity (API 9: download-service).

| Flag | Description |
|------|-------------|
| `--activity-id INT` | Garmin activity ID (**required**) |
| `--output-dir PATH` | Directory to save the FIT file (default: current directory) |

The FIT file is saved as `{activityId}_ACTIVITY.fit`. To get the activity ID, use `activities search` first and read the `activityId` field from the results.

To parse the FIT file, use `fitdecode` (included in `requirements.txt`). See API 9 in `garmin-api-spec.md` for details on the FIT format and what data it contains (GPS trackpoints, per-second HR/cadence/power, laps, etc.).

### activities gear

Get gear linked to an activity (API 10: gear-service).

| Flag | Description |
|------|-------------|
| `--activity-id INT` | Garmin activity ID (**required**) |

Returns an empty array if no gear is linked.

### gear list

List all user gear (gear-service).

| Flag | Description |
|------|-------------|
| `--status TEXT` | Filter: `ACTIVE` (default), `RETIRED`, or `ALL` |
| `--gear-type TEXT` | Filter by gear type (e.g. `SHOES`) |
| `--start INT` | Pagination offset (default: 0) |
| `--limit INT` | Max results (default: 50) |

Returns gear objects with brand, usage stats (distance, duration, days used), retirement threshold (`maxUsageDistanceMeters`), and retire date (for retired gear).

### metrics hill-score

Get daily hill score stats (API 3: metrics-service).

| Flag | Description |
|------|-------------|
| `--start-date DATE` | Start date, YYYY-MM-DD (**required**) |
| `--end-date DATE` | End date, YYYY-MM-DD (**required**) |
| `--aggregation TEXT` | Aggregation granularity (default: `daily`) |

### metrics endurance-score

Get endurance score stats (API 4: metrics-service).

| Flag | Description |
|------|-------------|
| `--start-date DATE` | Start date, YYYY-MM-DD (**required**) |
| `--end-date DATE` | End date, YYYY-MM-DD (**required**) |
| `--aggregation TEXT` | Aggregation granularity (default: `weekly`) |

### sleep stats

Get daily sleep summaries for a date range (API 5: sleep-service).

| Flag | Description |
|------|-------------|
| `--start-date DATE` | Start date, YYYY-MM-DD, inclusive (**required**) |
| `--end-date DATE` | End date, YYYY-MM-DD, inclusive (**required**) |

### sleep detail

Get full single-night sleep data with time-series (API 6: sleep-service).

| Flag | Description |
|------|-------------|
| `--date DATE` | Wake-up date, YYYY-MM-DD (**required**) |
| `--non-sleep-buffer INT` | Minutes of pre/post-sleep data to include (default: 60) |

### wellness daily-summary

Get daily wellness summary (garth: usersummary-service).

| Flag | Description |
|------|-------------|
| `--date DATE` | Date, YYYY-MM-DD (**required**) |

Returns steps, calories, HR, stress, body battery, SpO2, floors, intensity minutes, respiration — all in one call.

### wellness heart-rate

Get daily heart rate time-series (garth: wellness-service).

| Flag | Description |
|------|-------------|
| `--date DATE` | Date, YYYY-MM-DD (**required**) |

Returns `heartRateValues` array: `[[timestamp_ms, hr_value], ...]`

### wellness stress-weekly

Get weekly stress aggregates (garth: usersummary-service).

| Flag | Description |
|------|-------------|
| `--end-date DATE` | End date, YYYY-MM-DD (**required**) |
| `--num-weeks INT` | Number of weeks to retrieve, auto-paginates beyond 52 (**required**) |

### wellness stress-daily

Get daily stress aggregates (garth: usersummary-service).

| Flag | Description |
|------|-------------|
| `--start-date DATE` | Start date, YYYY-MM-DD (**required**) |
| `--end-date DATE` | End date, YYYY-MM-DD (**required**) |

Auto-paginates beyond the 28-day API limit.

### wellness hrv

Get nightly HRV readings and baseline (garth: hrv-service).

| Flag | Description |
|------|-------------|
| `--date DATE` | Date, YYYY-MM-DD (**required**) |

### wellness weight

Get weight entries for a date range (garth: weight-service).

| Flag | Description |
|------|-------------|
| `--start-date DATE` | Start date, YYYY-MM-DD (**required**) |
| `--end-date DATE` | End date, YYYY-MM-DD (**required**) |

### wellness training-readiness

Get training readiness score (garth: metrics-service).

| Flag | Description |
|------|-------------|
| `--date DATE` | Date, YYYY-MM-DD (**required**) |

### wellness training-status

Get training status and load (garth: mobile-gateway).

| Flag | Description |
|------|-------------|
| `--date DATE` | Date, YYYY-MM-DD (**required**) |

### calendar month

Get monthly calendar with all item types (API 7: calendar-service).

| Flag | Description |
|------|-------------|
| `--year INT` | Calendar year (**required**) |
| `--month INT` | Calendar month, 1-indexed: 1=Jan, 12=Dec (**required**). The CLI converts to 0-indexed for the API. |

### calendar note

Get full content of a calendar note (API 8: calendar-service).

| Flag | Description |
|------|-------------|
| `--note-id INT` | Note ID from calendar item (**required**) |

## Examples

```bash
# Search for running activities in January 2026
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py activities search --limit 20 --start 0 \
  --activity-type running --start-date 2026-01-01 --end-date 2026-01-31

# Search for pickleball activities (use --search for free-text matching)
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py activities search --limit 100 --start 0 \
  --search pickleball --start-date 2025-01-01 --end-date 2026-03-02

# Get detail for a specific activity
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py activities detail --activity-id 18000000001

# Download FIT file to /tmp
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py activities download --activity-id 18000000001 --output-dir /tmp

# Get gear linked to an activity
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py activities gear --activity-id 18000000002

# List all active shoes
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py gear list --gear-type SHOES

# List retired shoes
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py gear list --gear-type SHOES --status RETIRED

# Save output to file (global flag BEFORE subcommand)
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py --output file.json activities search --limit 5 --start 0
```

## Gotchas

### `--start 0` is required for `activities search`

Easy to forget. The command will fail without it. Always include `--start 0` (or another offset) alongside `--limit`.

### Global flags must appear BEFORE the subcommand

This is an argparse limitation.

**Correct:** `python garmin_cli.py --output file.json activities search --limit 5 --start 0`
**Wrong:** `python garmin_cli.py activities search --limit 5 --output file.json`

### Activity type filtering

- `--activity-type` for parent types (e.g. `running`, `racket_sports`, `winter_sports`, `fitness_equipment`)
- `--activity-sub-type` for sub-types (e.g. `trail_running`, `tennis_v2`, `resort_skiing_snowboarding_ws`)
- `--activity-sub-type` requires `--activity-type`

**Sub-type keys are non-obvious** — they often don't match the common activity name (e.g. `tennis_v2` not `tennis`, `resort_skiing_snowboarding_ws` not `skiing`). When unsure of the key, use `--search` first and inspect `activityType.typeKey` in the response to discover the actual key. Note: `--search` does free-text matching on activity names, so results may include false positives — filter by `activityType.typeKey` to get exact matches.

**Parent/sub-type naming overlap** — some parent type keys are reused as sub-type `typeKey` values in response data. For example, `running` is both the parent type and the `typeKey` for road/generic runs. When the user says "running", they typically mean **all running** (the parent), not just the `running` sub-type. When breaking down sub-types, label the `running` typeKey as "road/generic running" to avoid ambiguity.

### Cookie shell escaping (cookie auth only)

The Garmin cookie contains `|`, `*`, `~`, and other characters that break shell variable expansion. Write the cookie to a temp file using a Bash heredoc (`cat > /tmp/garmin_cookie.txt << 'EOF'`), then pass it to the CLI via `--cookie "$(cat /tmp/garmin_cookie.txt)"`. Do NOT paste the cookie directly into a shell `export` command.
