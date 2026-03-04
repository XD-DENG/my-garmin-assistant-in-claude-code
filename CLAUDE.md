# Garmin Data Project

## Garmin Connect CLI

To access Garmin Connect data, use the CLI at `garmin_cli.py`. Run with `python garmin_cli.py` (using the venv described in README.md). If needed to install dependencies, follow the instruciton in README.md.

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

- **Global flags (`--output`, `--cookie`, `--csrf-token`) must appear BEFORE the subcommand**. This is an argparse limitation. Example: `python garmin_cli.py --output file.json activities search --limit 5 --start 0` (correct) vs `... activities search --limit 5 --output file.json` (wrong — argparse error).

- **Activity type filtering uses two flags**: `--activity-type` for parent types (e.g. `running`, `racket_sports`, `winter_sports`, `fitness_equipment`) and `--activity-sub-type` for sub-types (e.g. `trail_running`, `tennis_v2`, `resort_skiing_snowboarding_ws`). Use `--activity-type` alone to get all activities in a category, or add `--activity-sub-type` to narrow down. `--activity-sub-type` requires `--activity-type`.

- **Sub-type keys are non-obvious** — they often don't match the common activity name (e.g. `tennis_v2` not `tennis`, `resort_skiing_snowboarding_ws` not `skiing`). When unsure of the key, use `--search` first and inspect `activityType.typeKey` in the response to discover the actual key. Note: `--search` does free-text matching on activity names, so results may include false positives — filter by `activityType.typeKey` to get exact matches.

- **Parent/sub-type naming overlap** — some parent type keys are reused as sub-type `typeKey` values in response data. For example, `running` is both the parent type and the `typeKey` for road/generic runs. When the user says "running", they typically mean **all running** (the parent), not just the `running` sub-type. When breaking down sub-types, label the `running` typeKey as "road/generic running" to avoid ambiguity.

## API Spec

Full API documentation is in `garmin-api-spec.md`. Reference this when adding new endpoints to the CLI.
