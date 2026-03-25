---
name: my-garmin-assistant
description: Access Garmin Connect data for activities, wellness, sleep, training analysis, and fitness metrics. Use when the user asks about workouts, heart rate, HRV, stress, weight, training readiness, running analysis, or any Garmin data.
argument-hint: "[query or command]"
allowed-tools: Bash, Read, Grep, Glob, Agent
---

# Garmin Connect Assistant

Access Garmin Connect data via a Python CLI that wraps 11 Garmin APIs plus supplementary garth wellness endpoints. Outputs raw JSON for analysis.

## Running the CLI

```bash
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py <command>
```

### Python setup

The CLI requires a Python venv with dependencies installed:

1. Check if `${CLAUDE_SKILL_DIR}/scripts/venv/` exists
2. If yes, activate it: `source ${CLAUDE_SKILL_DIR}/scripts/venv/bin/activate`
3. If no, create it:
   ```bash
   python3 -m venv ${CLAUDE_SKILL_DIR}/scripts/venv
   source ${CLAUDE_SKILL_DIR}/scripts/venv/bin/activate
   pip install -r ${CLAUDE_SKILL_DIR}/scripts/requirements.txt
   ```
4. Then run: `python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py <command>`

Alternative: if `uv` is available, skip venv entirely:
```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py <command>
```

## Authentication

Auth priority: CLI flags > env vars > `~/.garmin_tokens/` (OAuth).

**Preferred method — OAuth login:**
1. Run `python ${CLAUDE_SKILL_DIR}/scripts/garmin_auth.py` — prompts for Garmin email + password
2. Tokens are saved to `~/.garmin_tokens/` (OAuth1 lasts ~1 year, OAuth2 auto-refreshes)
3. The CLI reads tokens automatically — no flags or env vars needed
4. Re-run `garmin_auth.py` if the OAuth1 token eventually expires (~1 year)

When the user gets auth errors, tell them to re-run `python ${CLAUDE_SKILL_DIR}/scripts/garmin_auth.py`.

**Fallback method — manual cookie auth:**
Provide credentials via env vars (`GARMIN_COOKIE`, `GARMIN_CSRF_TOKEN`) or CLI flags (`--cookie`, `--csrf-token`). Ask the user to paste the curl command from browser dev tools, then parse the cookie and token from it.

**Cookie shell escaping** (only relevant for cookie auth): The Garmin cookie contains `|`, `*`, `~`, and other characters that break shell variable expansion. Write the cookie to a temp file using a Bash heredoc (`cat > /tmp/garmin_cookie.txt << 'EOF'`), then pass it to the CLI via `--cookie "$(cat /tmp/garmin_cookie.txt)"`. Do NOT paste the cookie directly into a shell `export` command.

## Quick reference — common commands

```bash
# Search activities
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py activities search --limit 10 --start 0 --activity-type running

# Activity detail
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py activities detail --activity-id <ID>

# Download FIT file
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py activities download --activity-id <ID> --output-dir /tmp

# Daily wellness summary (steps, calories, HR, stress, body battery, SpO2)
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py wellness daily-summary --date 2026-03-09

# Heart rate time-series
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py wellness heart-rate --date 2026-03-09

# HRV + baseline
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py wellness hrv --date 2026-03-09

# Weight
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py wellness weight --start-date 2026-02-09 --end-date 2026-03-09

# Training readiness
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py wellness training-readiness --date 2026-03-09

# Training status (weekly load, VO2 trend, ACWR)
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py wellness training-status --date 2026-03-09

# Stress (weekly/daily)
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py wellness stress-weekly --end-date 2026-03-09 --num-weeks 12
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py wellness stress-daily --start-date 2026-03-03 --end-date 2026-03-09

# Sleep
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py sleep stats --start-date 2026-02-21 --end-date 2026-02-27
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py sleep detail --date 2026-03-09

# Gear
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py gear list --gear-type SHOES
python ${CLAUDE_SKILL_DIR}/scripts/garmin_cli.py activities gear --activity-id <ID>
```

## Key gotchas

- **`--start 0` is required for `activities search`** — the command will fail without it. Always include `--start 0` (or another offset) alongside `--limit`.

- **Global flags (`--output`, `--cookie`, `--csrf-token`) must appear BEFORE the subcommand.** This is an argparse limitation. Example: `python garmin_cli.py --output file.json activities search --limit 5 --start 0` (correct) vs `... activities search --limit 5 --output file.json` (wrong).

- **Activity type filtering uses two flags**: `--activity-type` for parent types (e.g. `running`, `racket_sports`, `winter_sports`, `fitness_equipment`) and `--activity-sub-type` for sub-types (e.g. `trail_running`, `tennis_v2`, `resort_skiing_snowboarding_ws`). `--activity-sub-type` requires `--activity-type`.

- **Sub-type keys are non-obvious** — they often don't match common names (e.g. `tennis_v2` not `tennis`). When unsure, use `--search` first and inspect `activityType.typeKey` in the response.

- **Parent/sub-type naming overlap** — `running` is both the parent type and the `typeKey` for road/generic runs. When the user says "running", they typically mean **all running** (the parent). Label the `running` typeKey as "road/generic running" to avoid ambiguity.

## FIT file parsing

To parse downloaded FIT files, use `fitdecode` (included in `requirements.txt`):

```python
import fitdecode
with fitdecode.FitReader('/tmp/<activityId>_ACTIVITY.fit') as fit:
    for frame in fit:
        if isinstance(frame, fitdecode.FitDataMessage):
            if frame.name == 'record':
                # Per-second data: HR, cadence, power, GPS, etc.
                pass
```

## Training analysis & memory

Memory files are stored at `~/.claude/memory/garmin/`. This directory contains:
- `MEMORY.md` — index of all memory files (user profile, analysis patterns, technical notes)
- `running-profile.md` — detailed race history, upcoming races, training patterns, recovery benchmarks
- Other memory files as needed (e.g. feedback on workflow preferences)

After any training analysis or advice conversation, **automatically save key findings to memory** before the conversation ends:

- **After analyzing a race or training run**: Update `~/.claude/memory/garmin/running-profile.md` with distance, time, elevation, avg HR, pacing breakdown, key performance insights, comparisons to previous efforts
- **After giving training advice**: Update `~/.claude/memory/garmin/running-profile.md` with plan changes, workout recommendations, target paces/HR zones, injury concerns
- **After analyzing wellness/fitness trends**: Update `~/.claude/memory/garmin/MEMORY.md` user profile with VO2 Max, resting HR, HRV baseline, body weight (with date), notable trend changes
- **After race planning discussions**: Update `~/.claude/memory/garmin/running-profile.md` with race details, pacing strategy, HR targets, nutrition plan, gear decisions, training priorities

General rules:
- Updates happen automatically — do not wait to be asked
- Always include dates so information doesn't go stale
- Preserve existing content — append or revise, don't overwrite unrelated sections
- If new analysis contradicts earlier memory, update the old entry rather than creating duplicates
- When fetching data from multiple Garmin endpoints, write a single temp Python script instead of many individual CLI calls to minimize permission prompts

## Additional resources

- For complete CLI command reference with all flags, see [references/cli-reference.md](references/cli-reference.md)
- For full API documentation, see [references/garmin-api-spec.md](references/garmin-api-spec.md)
- For wellness/health API endpoints (garth), see [references/garmin-api-from-garth.md](references/garmin-api-from-garth.md)
