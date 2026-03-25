# My Garmin Assistant

A [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code/skills) that gives Claude access to your Garmin Connect data — activities, wellness, sleep, training analysis, and fitness metrics.

Once installed, Claude can automatically fetch and analyze your Garmin data when you ask about your workouts, heart rate, HRV, stress, weight, training readiness, and more. Works from any project.

## Installation

**Option A: Clone from GitHub**

```bash
git clone https://github.com/XD-DENG/my-garmin-assistant-in-claude-code.git ~/.claude/skills/my-garmin-assistant
```

**Option B: Copy from a local checkout**

```bash
mkdir -p ~/.claude/skills
cp -r /path/to/my-garmin-assistant ~/.claude/skills/my-garmin-assistant
```

### Install Python dependencies

```bash
cd ~/.claude/skills/my-garmin-assistant/scripts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Or, if you have [uv](https://docs.astral.sh/uv/) installed, skip the venv entirely — the CLI will auto-install dependencies on first run.

### Authenticate with Garmin

```bash
cd ~/.claude/skills/my-garmin-assistant/scripts
source venv/bin/activate
python garmin_auth.py
```

This prompts for your Garmin email and password. Tokens are saved to `~/.garmin_tokens/`. The OAuth1 token lasts ~1 year; OAuth2 tokens refresh automatically.

If you prefer manual cookie auth, see the [CLI reference](references/cli-reference.md#cookie-shell-escaping-cookie-auth-only).

## Usage

Once installed, you can:

**Let Claude invoke it automatically** — just ask about your Garmin data from any project:

```
How did my run go yesterday?
What's my HRV trend this month?
Show me my last 5 activities
```

**Or invoke it directly** with the skill name:

```
/my-garmin-assistant What's my training readiness today?
```

## What's included

| Directory | Contents |
|-----------|----------|
| `SKILL.md` | Skill definition — instructions Claude follows when accessing Garmin data |
| `scripts/` | Python CLI (`garmin_cli.py`) and OAuth auth script (`garmin_auth.py`) |
| `references/` | CLI command reference, Garmin API specs (loaded on-demand by Claude) |

## Available data

- **Activities**: search, detail, FIT file download, linked gear
- **Wellness**: daily summary, heart rate, HRV, stress (daily/weekly), weight, training readiness, training status
- **Sleep**: daily summaries, single-night detail with time-series
- **Metrics**: hill score, endurance score
- **Calendar**: monthly view, note content
- **Gear**: list all gear, filter by type/status

See [references/cli-reference.md](references/cli-reference.md) for the full command reference.

## API Reference

- [references/garmin-api-spec.md](references/garmin-api-spec.md) — Primary API documentation (activities, sleep, scores, calendar, FIT file download)
- [references/garmin-api-from-garth.md](references/garmin-api-from-garth.md) — Supplementary wellness/health endpoints extracted from the [garth](https://github.com/matin/garth) Python package
