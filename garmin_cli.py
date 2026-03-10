#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests", "brotli", "requests-oauthlib"]
# ///
"""
Garmin Connect CLI — A command-line tool for accessing Garmin Connect APIs.

This tool wraps 10 Garmin Connect APIs plus supplementary garth endpoints,
and outputs raw JSON to stdout (or downloads binary files for the FIT
download command). It is designed for programmatic use (piping, scripting,
LLM tool-use).

================================================================================
AUTHENTICATION
================================================================================

Recommended: run `python garmin_auth.py` to log in with your Garmin email
and password. Tokens are saved to ~/.garmin_tokens/ and the CLI uses them
automatically. OAuth1 token lasts ~1 year; OAuth2 refreshes automatically.

Alternative: provide Cookie + CSRF token manually (from browser dev tools):
  export GARMIN_COOKIE='your_cookie_value'
  export GARMIN_CSRF_TOKEN='your_csrf_token_value'

Or via CLI flags (overrides everything):
  python garmin_cli.py --cookie '...' --csrf-token '...' <command>

Auth priority: CLI flags > env vars > ~/.garmin_tokens/ (OAuth).

================================================================================
SUBCOMMANDS
================================================================================

activities search   — Search/filter activities (API 1: activitylist-service)
  --limit INT          Max results to return (required)
  --start INT          Pagination offset, 0-indexed (required)
  --search TEXT        Free-text search across activity names
  --activity-type TEXT Parent activity type key (e.g. "running", "racket_sports",
                       "winter_sports", "fitness_equipment").
  --activity-sub-type TEXT  Activity sub-type key (e.g. "trail_running", "tennis_v2",
                       "resort_skiing_snowboarding_ws"). Requires --activity-type.
  --start-date DATE   Filter start date, YYYY-MM-DD, inclusive
  --end-date DATE     Filter end date, YYYY-MM-DD, inclusive
  --exclude-children  Exclude child activities (multi-sport sub-activities)

activities detail   — Get full detail for a single activity (API 2: activity-service)
  --activity-id INT    Garmin activity ID (required)

activities download — Download original FIT file for an activity (API 9: download-service)
  --activity-id INT    Garmin activity ID (required)
  --output-dir PATH    Directory to save the FIT file (default: current directory)

activities gear     — Get gear linked to an activity (API 10: gear-service)
  --activity-id INT    Garmin activity ID (required)

metrics hill-score  — Get daily hill score stats (API 3: metrics-service)
  --start-date DATE   Start date, YYYY-MM-DD (required)
  --end-date DATE     End date, YYYY-MM-DD (required)
  --aggregation TEXT   Aggregation granularity (default: "daily")

metrics endurance-score — Get endurance score stats (API 4: metrics-service)
  --start-date DATE   Start date, YYYY-MM-DD (required)
  --end-date DATE     End date, YYYY-MM-DD (required)
  --aggregation TEXT   Aggregation granularity (default: "weekly")

sleep stats         — Get daily sleep summaries for a date range (API 5: sleep-service)
  --start-date DATE   Start date, YYYY-MM-DD, inclusive (required)
  --end-date DATE     End date, YYYY-MM-DD, inclusive (required)

sleep detail        — Get full single-night sleep data with time-series (API 6: sleep-service)
  --date DATE          Wake-up date, YYYY-MM-DD (required)
  --non-sleep-buffer INT  Minutes of pre/post-sleep data to include (default: 60)

wellness stress-weekly — Get weekly stress aggregates (garth: usersummary-service)
  --end-date DATE      End date, YYYY-MM-DD (required)
  --num-weeks INT      Number of weeks to retrieve, auto-paginates beyond 52 (required)

wellness stress-daily — Get daily stress aggregates (garth: usersummary-service)
  --start-date DATE    Start date, YYYY-MM-DD (required)
  --end-date DATE      End date, YYYY-MM-DD (required)
                       Auto-paginates beyond the 28-day API limit.

wellness hrv          — Get nightly HRV readings and baseline (garth: hrv-service)
  --date DATE          Date, YYYY-MM-DD (required)

wellness weight       — Get weight entries for a date range (garth: weight-service)
  --start-date DATE    Start date, YYYY-MM-DD (required)
  --end-date DATE      End date, YYYY-MM-DD (required)

wellness training-readiness — Get training readiness score (garth: metrics-service)
  --date DATE          Date, YYYY-MM-DD (required)

wellness training-status — Get training status and load (garth: mobile-gateway)
  --date DATE          Date, YYYY-MM-DD (required)

calendar month      — Get monthly calendar with all item types (API 7: calendar-service)
  --year INT           Calendar year (required)
  --month INT          Calendar month, 1-indexed: 1=Jan, 12=Dec (required)
                       Note: the API uses 0-indexed months internally; the CLI converts for you.

calendar note       — Get full content of a calendar note (API 8: calendar-service)
  --note-id INT        Note ID from calendar item (required)

================================================================================
GLOBAL FLAGS (must appear BEFORE subcommand)
================================================================================

  --cookie TEXT        Cookie header value (overrides GARMIN_COOKIE env var)
  --csrf-token TEXT    CSRF token value (overrides GARMIN_CSRF_TOKEN env var)
  --output FILE        Write JSON output to a file instead of stdout

================================================================================
EXAMPLES
================================================================================

# Search for running activities (parent type) in January 2026
python garmin_cli.py activities search --limit 20 --start 0 \\
  --activity-type running --start-date 2026-01-01 --end-date 2026-01-31

# Search for pickleball activities (sub-type — use --search, not --activity-type)
python garmin_cli.py activities search --limit 100 --start 0 \\
  --search pickleball --start-date 2025-01-01 --end-date 2026-03-02

# Get detail for a specific activity
python garmin_cli.py activities detail --activity-id 21942154782

# Download original FIT file for an activity
python garmin_cli.py activities download --activity-id 21942154782

# Download FIT file to a specific directory
python garmin_cli.py activities download --activity-id 21942154782 --output-dir /tmp

# Get gear linked to an activity (e.g. shoes)
python garmin_cli.py activities gear --activity-id 21993647638

# Get hill score for a date range
python garmin_cli.py metrics hill-score --start-date 2026-01-30 --end-date 2026-02-26

# Get endurance score (weekly aggregation)
python garmin_cli.py metrics endurance-score --start-date 2025-12-06 --end-date 2026-02-27

# Get sleep stats for a week
python garmin_cli.py sleep stats --start-date 2026-02-21 --end-date 2026-02-27

# Get detailed sleep data for one night
python garmin_cli.py sleep detail --date 2026-02-26

# Get January 2026 calendar
python garmin_cli.py calendar month --year 2026 --month 1

# Get a note's full content
python garmin_cli.py calendar note --note-id 126088664

# Get weekly stress averages for the last 12 weeks
python garmin_cli.py wellness stress-weekly --end-date 2026-03-09 --num-weeks 12

# Get daily stress breakdown for a week
python garmin_cli.py wellness stress-daily --start-date 2026-03-03 --end-date 2026-03-09

# Get nightly HRV readings and baseline
python garmin_cli.py wellness hrv --date 2026-03-09

# Get weight entries for a month
python garmin_cli.py wellness weight --start-date 2026-02-09 --end-date 2026-03-09

# Get training readiness score for today
python garmin_cli.py wellness training-readiness --date 2026-03-09

# Get training status (load, VO2 trend, ACWR)
python garmin_cli.py wellness training-status --date 2026-03-09

# Save output to a file (--output is a global flag, must come before subcommand)
python garmin_cli.py --output activities.json activities search --limit 5 --start 0

# Using CLI flags for auth instead of env vars
python garmin_cli.py --cookie 'my_cookie' --csrf-token 'my_token' \\
  activities search --limit 5 --start 0

================================================================================
EXTENDING THIS TOOL
================================================================================

To add a new Garmin Connect API:
1. Add a new method to the GarminClient class following the existing pattern:
   - Method name: descriptive verb_noun (e.g., get_heart_rate)
   - Docstring: document endpoint URL, parameters, and return type
   - Implementation: call self._get() with the URL and params
2. Add a subparser setup function (e.g., _setup_heart_rate_parser)
   - Add argparse arguments matching the API parameters
   - Set the 'func' default to a lambda that calls the new GarminClient method
3. Register the subparser in build_parser() under the appropriate group

================================================================================
DEPENDENCIES
================================================================================

  pip install requests
  # Or run directly with uv (auto-installs dependencies via inline metadata):
  uv run garmin_cli.py --help

Python 3.9+ required.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests


BASE_URL_COOKIE = "https://connect.garmin.com/gc-api"
BASE_URL_OAUTH = "https://connectapi.garmin.com"


class GarminClient:
    """HTTP client for Garmin Connect APIs.

    Supports two auth modes:
      - Cookie-based: uses Cookie + CSRF token headers against connect.garmin.com
      - OAuth-based: uses Bearer token against connectapi.garmin.com (recommended)
    """

    def __init__(
        self,
        cookie: str | None = None,
        csrf_token: str | None = None,
        oauth1_token: dict | None = None,
        oauth2_token: dict | None = None,
    ):
        self.session = requests.Session()
        self.oauth1_token = oauth1_token
        self.oauth2_token = oauth2_token

        if cookie:
            # Cookie-based auth (web browser flow)
            self.base_url = BASE_URL_COOKIE
            self.session.headers.update({
                "Cookie": cookie,
                "Connect-Csrf-Token": csrf_token or "",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
            })
        else:
            # OAuth-based auth (mobile app flow)
            self.base_url = BASE_URL_OAUTH
            self._ensure_oauth2()
            self.session.headers.update({
                "Authorization": f"Bearer {self.oauth2_token['access_token']}",
                "User-Agent": "com.garmin.android.apps.connectmobile",
            })

    def _ensure_oauth2(self) -> None:
        """Refresh OAuth2 token if expired, using the OAuth1 token."""
        if not self.oauth2_token or self.oauth2_token.get("expires_at", 0) < time.time():
            if not self.oauth1_token:
                print("Error: OAuth2 token expired and no OAuth1 token to refresh.", file=sys.stderr)
                sys.exit(1)
            print("OAuth2 token expired, refreshing...", file=sys.stderr)
            # Import here to avoid requiring requests-oauthlib for cookie auth
            from garmin_auth import exchange_oauth2, save_tokens
            self.oauth2_token = exchange_oauth2(self.oauth1_token)
            save_tokens(self.oauth1_token, self.oauth2_token)
            self.session.headers["Authorization"] = f"Bearer {self.oauth2_token['access_token']}"

    def _get(self, url: str, params: dict[str, Any] | None = None) -> Any:
        """Make a GET request and return parsed JSON."""
        if self.oauth1_token:
            self._ensure_oauth2()
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        if not resp.text.strip():
            print("Error: Empty response body. Session may have expired — re-run: python garmin_auth.py", file=sys.stderr)
            sys.exit(1)
        try:
            return resp.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Error: Non-JSON response — {resp.text[:500]}", file=sys.stderr)
            sys.exit(1)

    def _get_binary(self, url: str) -> bytes:
        """Make a GET request and return raw bytes (for binary downloads)."""
        if self.oauth1_token:
            self._ensure_oauth2()
        resp = self.session.get(url)
        resp.raise_for_status()
        if not resp.content:
            print("Error: Empty response body. Session may have expired — re-run: python garmin_auth.py", file=sys.stderr)
            sys.exit(1)
        return resp.content

    # ── API 1: Activity List Search ──────────────────────────────────────

    def search_activities(
        self,
        limit: int,
        start: int,
        search: str | None = None,
        activity_type: str | None = None,
        activity_sub_type: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        exclude_children: bool | None = None,
    ) -> list[dict]:
        """Search and filter activities.

        Endpoint: GET {BASE}/activitylist-service/activities/search/activities

        Args:
            limit: Max number of activities to return.
            start: Pagination offset (0-indexed).
            search: Free-text search across activity names.
            activity_type: Filter by parent activity type key (e.g. "running",
                "racket_sports", "winter_sports", "fitness_equipment").
            activity_sub_type: Filter by activity sub-type key (e.g.
                "trail_running", "tennis_v2", "resort_skiing_snowboarding_ws").
                Requires activity_type to be set.
            start_date: Filter start date, YYYY-MM-DD, inclusive.
            end_date: Filter end date, YYYY-MM-DD, inclusive.
            exclude_children: Whether to exclude child activities (multi-sport).

        Returns:
            JSON array of activity objects. Each object contains fields like
            activityId, activityName, startTimeLocal, distance (meters),
            duration (seconds), averageHR, elevationGain, etc.
        """
        params: dict[str, Any] = {"limit": limit, "start": start}
        if search is not None:
            params["search"] = search
        if activity_type is not None:
            params["activityType"] = activity_type
        if activity_sub_type is not None:
            params["activitySubType"] = activity_sub_type
        if start_date is not None:
            params["startDate"] = start_date
        if end_date is not None:
            params["endDate"] = end_date
        if exclude_children is not None:
            params["excludeChildren"] = str(exclude_children).lower()
        return self._get(
            f"{self.base_url}/activitylist-service/activities/search/activities",
            params=params,
        )

    # ── API 2: Single Activity Detail ────────────────────────────────────

    def get_activity(self, activity_id: int) -> dict:
        """Get full detail for a single activity.

        Endpoint: GET {BASE}/activity-service/activity/{activityId}

        Args:
            activity_id: Garmin activity ID (numeric).

        Returns:
            JSON object with nested DTOs: activityTypeDTO, metadataDTO,
            summaryDTO (distance, speed, HR, power, elevation, etc.),
            and splitSummaries array with per-split metrics.
        """
        return self._get(
            f"{self.base_url}/activity-service/activity/{activity_id}"
        )

    # ── API 9: Activity File Download ─────────────────────────────────────

    def download_activity(self, activity_id: int, output_dir: str = ".") -> str:
        """Download the original FIT file for an activity.

        Endpoint: GET {BASE}/download-service/files/activity/{activityId}

        Args:
            activity_id: Garmin activity ID (numeric).
            output_dir: Directory to save the extracted FIT file (default: ".").

        Returns:
            Path to the extracted FIT file.
        """
        import io
        import zipfile

        data = self._get_binary(
            f"{self.base_url}/download-service/files/activity/{activity_id}"
        )

        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            fit_names = [n for n in zf.namelist() if n.endswith(".fit")]
            if not fit_names:
                print("Error: ZIP contains no .fit files.", file=sys.stderr)
                sys.exit(1)
            zf.extract(fit_names[0], path=out)
            return str(out / fit_names[0])

    # ── API 10: Activity Gear ────────────────────────────────────────────

    def get_activity_gear(self, activity_id: int) -> list[dict]:
        """Get gear linked to an activity.

        Endpoint: GET {BASE}/gear-service/activity/v2/{activityId}

        Args:
            activity_id: Garmin activity ID (numeric).

        Returns:
            JSON array of gear objects. Each object contains uuid, gearType
            (e.g. "SHOES"), status, name, brand, usageType, maxUsageDistanceMeters,
            firstUseDate, numActivitiesLinked, durationUsedSeconds,
            distanceUsedMeters, daysUsed. Returns empty array if no gear linked.
        """
        return self._get(
            f"{self.base_url}/gear-service/activity/v2/{activity_id}"
        )

    # ── API 3: Hill Score Stats ──────────────────────────────────────────

    def get_hill_score(
        self,
        start_date: str,
        end_date: str,
        aggregation: str = "daily",
    ) -> dict:
        """Get daily hill score stats.

        Endpoint: GET {BASE}/metrics-service/metrics/hillscore/stats

        Args:
            start_date: Start date, YYYY-MM-DD.
            end_date: End date, YYYY-MM-DD.
            aggregation: Granularity of data points (default: "daily").

        Returns:
            JSON object with periodAvgScore, maxScore, and hillScoreDTOList
            array (one entry per day with overallScore, strengthScore,
            enduranceScore on a 0-100 scale).
        """
        return self._get(
            f"{self.base_url}/metrics-service/metrics/hillscore/stats",
            params={
                "startDate": start_date,
                "endDate": end_date,
                "aggregation": aggregation,
            },
        )

    # ── API 4: Endurance Score Stats ─────────────────────────────────────

    def get_endurance_score(
        self,
        start_date: str,
        end_date: str,
        aggregation: str = "weekly",
    ) -> dict:
        """Get endurance score stats.

        Endpoint: GET {BASE}/metrics-service/metrics/endurancescore/stats

        Args:
            start_date: Start date, YYYY-MM-DD.
            end_date: End date, YYYY-MM-DD.
            aggregation: Granularity (default: "weekly", also supports "daily").

        Returns:
            JSON object with avg, max scores (scale ~3500-10500), groupMap
            (weekly entries with contribution breakdowns by activity type),
            and enduranceScoreDTO (current day snapshot with classification
            tiers: Intermediate/Trained/WellTrained/Expert/Superior/Elite).
        """
        return self._get(
            f"{self.base_url}/metrics-service/metrics/endurancescore/stats",
            params={
                "startDate": start_date,
                "endDate": end_date,
                "aggregation": aggregation,
            },
        )

    # ── API 5: Sleep Stats ───────────────────────────────────────────────

    def get_sleep_stats(self, start_date: str, end_date: str) -> dict:
        """Get daily sleep summaries for a date range.

        Endpoint: GET {BASE}/sleep-service/stats/sleep/daily/{startDate}/{endDate}

        Args:
            start_date: Start date, YYYY-MM-DD, inclusive.
            end_date: End date, YYYY-MM-DD, inclusive.

        Returns:
            JSON object with overallStats (averages for the period) and
            individualStats array (per-night: sleepScore, sleepScoreQuality,
            totalSleepTimeInSeconds, remTime, deepTime, lightTime, awakeTime,
            avgHeartRate, avgOvernightHrv, spO2, bodyBatteryChange, etc.).
        """
        return self._get(
            f"{self.base_url}/sleep-service/stats/sleep/daily/{start_date}/{end_date}"
        )

    # ── API 6: Daily Sleep Detail ────────────────────────────────────────

    def get_sleep_detail(
        self,
        date: str,
        non_sleep_buffer_minutes: int = 60,
    ) -> dict:
        """Get full single-night sleep data with time-series.

        Endpoint: GET {BASE}/sleep-service/sleep/dailySleepData

        Args:
            date: Wake-up date, YYYY-MM-DD.
            non_sleep_buffer_minutes: Minutes of pre/post-sleep data to
                include in time-series arrays (default: 60).

        Returns:
            JSON object with dailySleepDTO (rich summary including sleep
            score component breakdown, sleep need adjustments, nap DTOs),
            plus 7 time-series arrays: sleepMovement (1-min), sleepLevels
            (sleep stage segments: 0=deep, 1=light, 2=REM, 3=awake),
            sleepHeartRate (2-min), sleepStress (3-min), sleepBodyBattery
            (3-min), hrvData (5-min), wellnessEpochSPO2DataDTOList (1-min).
        """
        return self._get(
            f"{self.base_url}/sleep-service/sleep/dailySleepData",
            params={
                "date": date,
                "nonSleepBufferMinutes": non_sleep_buffer_minutes,
            },
        )

    # ── API 7: Monthly Calendar ──────────────────────────────────────────

    def get_calendar_month(self, year: int, month: int) -> dict:
        """Get monthly calendar with all item types.

        Endpoint: GET {BASE}/calendar-service/year/{year}/month/{month}

        Note: The API uses 0-indexed months (0=Jan, 11=Dec). This method
        accepts 1-indexed months (1=Jan, 12=Dec) and converts internally.

        Args:
            year: Calendar year (e.g. 2026).
            month: Calendar month, 1-indexed (1=January, 12=December).

        Returns:
            JSON object with calendarItems array containing all item types:
            activities (with summary metrics), goals (paired start/end),
            weight entries (grams), naps, notes (title only — use get_note
            for full content), and events. Note: activity duration is in
            milliseconds and distance in centimeters (different from other APIs).
        """
        api_month = month - 1  # Convert 1-indexed to 0-indexed
        return self._get(
            f"{self.base_url}/calendar-service/year/{year}/month/{api_month}"
        )

    # ── API 8: Calendar Note Detail ──────────────────────────────────────

    def get_note(self, note_id: int) -> dict:
        """Get full content of a calendar note.

        Endpoint: GET {BASE}/calendar-service/note/{noteId}

        Args:
            note_id: Note ID from a calendar item's 'id' field (API 7).

        Returns:
            JSON object with id, noteName, content (full body text,
            may be multi-line and contain Chinese characters), and date.
        """
        return self._get(
            f"{self.base_url}/calendar-service/note/{note_id}"
        )

    # ── Wellness: Weekly Stress (garth: usersummary-service) ─────────────

    def get_stress_weekly(self, end_date: str, num_weeks: int) -> list[dict]:
        """Get weekly stress aggregates for a date range.

        Endpoint: GET {BASE}/usersummary-service/stats/stress/weekly/{endDate}/{numWeeks}

        Args:
            end_date: End date, YYYY-MM-DD.
            num_weeks: Number of weeks to retrieve (max 52 per request;
                this method automatically paginates if num_weeks > 52).

        Returns:
            JSON array of weekly entries: [{ calendarDate, value }, ...]
            sorted ascending by date. value is weekly avg stress (0-100).
        """
        from datetime import date, timedelta

        results: list[dict] = []
        end = date.fromisoformat(end_date)
        remaining = num_weeks

        while remaining > 0:
            batch = min(remaining, 52)
            url = f"{self.base_url}/usersummary-service/stats/stress/weekly/{end.isoformat()}/{batch}"
            batch_data = self._get(url)
            if batch_data:
                results = batch_data + results  # prepend (older data first)
            # Move end date back by batch weeks
            end = end - timedelta(weeks=batch)
            remaining -= batch

        return results

    # ── Wellness: Daily Stress (garth: usersummary-service) ──────────────

    def get_stress_daily(self, start_date: str, end_date: str) -> list[dict]:
        """Get daily stress aggregates for a date range.

        Endpoint: GET {BASE}/usersummary-service/stats/stress/daily/{startDate}/{endDate}

        Args:
            start_date: Start date, YYYY-MM-DD.
            end_date: End date, YYYY-MM-DD.
                Max 28 days per request; this method automatically paginates
                for longer ranges.

        Returns:
            JSON array of daily entries sorted ascending by date. Each entry:
            { calendarDate, overallStressLevel, restStressDuration,
              lowStressDuration, mediumStressDuration, highStressDuration }
            (durations in seconds, stress 0-100).
        """
        from datetime import date, timedelta

        results: list[dict] = []
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)

        while start <= end:
            batch_end = min(start + timedelta(days=27), end)
            url = f"{self.base_url}/usersummary-service/stats/stress/daily/{start.isoformat()}/{batch_end.isoformat()}"
            batch_data = self._get(url)
            if batch_data:
                results.extend(batch_data)
            start = batch_end + timedelta(days=1)

        return results

    # ── Wellness: HRV Detail (garth: hrv-service) ────────────────────────

    def get_hrv(self, date: str) -> dict:
        """Get nightly HRV readings and baseline for a single date.

        Endpoint: GET {BASE}/hrv-service/hrv/{date}

        Args:
            date: Date, YYYY-MM-DD.

        Returns:
            JSON object with hrvSummary (calendarDate, weeklyAvg, lastNightAvg,
            lastNight5MinHigh, status e.g. "BALANCED", baseline ranges),
            hrvReadings array [{hrvValue, readingTimeGMT, readingTimeLocal}, ...],
            and sleep window timestamps.
        """
        return self._get(f"{self.base_url}/hrv-service/hrv/{date}")

    # ── Wellness: Weight Range (garth: weight-service) ───────────────────

    def get_weight(self, start_date: str, end_date: str) -> dict:
        """Get weight entries for a date range.

        Endpoint: GET {BASE}/weight-service/weight/range/{startDate}/{endDate}

        Args:
            start_date: Start date, YYYY-MM-DD.
            end_date: End date, YYYY-MM-DD.

        Returns:
            JSON object with dailyWeightSummaries array. Each summary contains
            allWeightMetrics array with entries: weight (grams), bmi, bodyFat %,
            bodyWater %, boneMass (grams), muscleMass (grams), metabolicAge,
            visceralFat, sourceType, timestampGMT.
        """
        return self._get(
            f"{self.base_url}/weight-service/weight/range/{start_date}/{end_date}",
            params={"includeAll": "true"},
        )

    # ── Wellness: Training Readiness (garth: metrics-service) ────────────

    def get_training_readiness(self, date: str) -> list[dict]:
        """Get training readiness score and component breakdown for a date.

        Endpoint: GET {BASE}/metrics-service/metrics/trainingreadiness/{date}

        Args:
            date: Date, YYYY-MM-DD.

        Returns:
            JSON array (multiple contexts, e.g. AFTER_WAKEUP_RESET, CURRENT).
            Each entry: score (0-100), level (e.g. "PRIME", "HIGH"),
            feedbackShort/feedbackLong, component scores and percentages
            (sleepScore, recoveryTime, acuteLoad, hrvWeeklyAverage,
            stressHistoryFactorPercent, sleepHistoryFactorPercent).
            Filter for inputContext == "AFTER_WAKEUP_RESET" for morning readiness.
        """
        return self._get(
            f"{self.base_url}/metrics-service/metrics/trainingreadiness/{date}"
        )

    # ── Wellness: Training Status (garth: mobile-gateway) ────────────────

    def get_training_status(self, date: str) -> dict:
        """Get training status (load, VO2 trend, ACWR) for a date.

        Endpoint: GET {BASE}/mobile-gateway/usersummary/trainingstatus/latest/{date}

        Args:
            date: Date, YYYY-MM-DD.

        Returns:
            JSON object (deeply nested). Key data is under
            mostRecentTrainingStatus.payload.latestTrainingStatusData.{deviceId}:
            weeklyTrainingLoad, trainingStatus, trainingStatusFeedbackPhrase
            (e.g. "Productive"), loadTunnelMin/Max, fitnessTrend (VO2 max trend),
            acwrPercent, acwrStatus (e.g. "OPTIMAL"), dailyTrainingLoadAcute,
            dailyTrainingLoadChronic, dailyAcuteChronicWorkloadRatio.
        """
        return self._get(
            f"{self.base_url}/mobile-gateway/usersummary/trainingstatus/latest/{date}"
        )


# ── CLI Setup ────────────────────────────────────────────────────────────


def _setup_activities_search(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("search", help="Search/filter activities (API 1)")
    p.add_argument("--limit", type=int, required=True, help="Max results to return")
    p.add_argument("--start", type=int, required=True, help="Pagination offset (0-indexed)")
    p.add_argument("--search", help="Free-text search across activity names")
    p.add_argument("--activity-type", help='Parent activity type key (e.g. "running", "racket_sports", "winter_sports", "fitness_equipment").')
    p.add_argument("--activity-sub-type", help='Activity sub-type key (e.g. "trail_running", "tennis_v2"). Requires --activity-type.')
    p.add_argument("--start-date", help="Filter start date, YYYY-MM-DD, inclusive")
    p.add_argument("--end-date", help="Filter end date, YYYY-MM-DD, inclusive")
    p.add_argument("--exclude-children", action="store_true", default=None, help="Exclude child activities (multi-sport)")
    p.set_defaults(func=lambda client, args: client.search_activities(
        limit=args.limit,
        start=args.start,
        search=args.search,
        activity_type=args.activity_type,
        activity_sub_type=args.activity_sub_type,
        start_date=args.start_date,
        end_date=args.end_date,
        exclude_children=args.exclude_children if args.exclude_children else None,
    ))


def _setup_activities_detail(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("detail", help="Get full detail for a single activity (API 2)")
    p.add_argument("--activity-id", type=int, required=True, help="Garmin activity ID")
    p.set_defaults(func=lambda client, args: client.get_activity(
        activity_id=args.activity_id,
    ))


def _setup_activities_download(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("download", help="Download original FIT file for an activity (API 9)")
    p.add_argument("--activity-id", type=int, required=True, help="Garmin activity ID")
    p.add_argument("--output-dir", default=".", help="Directory to save the FIT file (default: current directory)")
    p.set_defaults(func=lambda client, args: client.download_activity(
        activity_id=args.activity_id,
        output_dir=args.output_dir,
    ))


def _setup_activities_gear(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("gear", help="Get gear linked to an activity (API 10)")
    p.add_argument("--activity-id", type=int, required=True, help="Garmin activity ID")
    p.set_defaults(func=lambda client, args: client.get_activity_gear(
        activity_id=args.activity_id,
    ))


def _setup_metrics_hill_score(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("hill-score", help="Get daily hill score stats (API 3)")
    p.add_argument("--start-date", required=True, help="Start date, YYYY-MM-DD")
    p.add_argument("--end-date", required=True, help="End date, YYYY-MM-DD")
    p.add_argument("--aggregation", default="daily", help='Aggregation granularity (default: "daily")')
    p.set_defaults(func=lambda client, args: client.get_hill_score(
        start_date=args.start_date,
        end_date=args.end_date,
        aggregation=args.aggregation,
    ))


def _setup_metrics_endurance_score(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("endurance-score", help="Get endurance score stats (API 4)")
    p.add_argument("--start-date", required=True, help="Start date, YYYY-MM-DD")
    p.add_argument("--end-date", required=True, help="End date, YYYY-MM-DD")
    p.add_argument("--aggregation", default="weekly", help='Aggregation granularity (default: "weekly")')
    p.set_defaults(func=lambda client, args: client.get_endurance_score(
        start_date=args.start_date,
        end_date=args.end_date,
        aggregation=args.aggregation,
    ))


def _setup_sleep_stats(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("stats", help="Get daily sleep summaries for a date range (API 5)")
    p.add_argument("--start-date", required=True, help="Start date, YYYY-MM-DD, inclusive")
    p.add_argument("--end-date", required=True, help="End date, YYYY-MM-DD, inclusive")
    p.set_defaults(func=lambda client, args: client.get_sleep_stats(
        start_date=args.start_date,
        end_date=args.end_date,
    ))


def _setup_sleep_detail(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("detail", help="Get full single-night sleep data with time-series (API 6)")
    p.add_argument("--date", required=True, help="Wake-up date, YYYY-MM-DD")
    p.add_argument("--non-sleep-buffer", type=int, default=60, help="Minutes of pre/post-sleep data (default: 60)")
    p.set_defaults(func=lambda client, args: client.get_sleep_detail(
        date=args.date,
        non_sleep_buffer_minutes=args.non_sleep_buffer,
    ))


def _setup_calendar_month(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("month", help="Get monthly calendar with all item types (API 7)")
    p.add_argument("--year", type=int, required=True, help="Calendar year (e.g. 2026)")
    p.add_argument("--month", type=int, required=True, help="Calendar month, 1-indexed (1=Jan, 12=Dec)")
    p.set_defaults(func=lambda client, args: client.get_calendar_month(
        year=args.year,
        month=args.month,
    ))


def _setup_wellness_stress_weekly(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("stress-weekly", help="Get weekly stress aggregates (garth: usersummary-service)")
    p.add_argument("--end-date", required=True, help="End date, YYYY-MM-DD")
    p.add_argument("--num-weeks", type=int, required=True, help="Number of weeks to retrieve (auto-paginates beyond 52)")
    p.set_defaults(func=lambda client, args: client.get_stress_weekly(
        end_date=args.end_date,
        num_weeks=args.num_weeks,
    ))


def _setup_wellness_stress_daily(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("stress-daily", help="Get daily stress aggregates (garth: usersummary-service)")
    p.add_argument("--start-date", required=True, help="Start date, YYYY-MM-DD")
    p.add_argument("--end-date", required=True, help="End date, YYYY-MM-DD")
    p.set_defaults(func=lambda client, args: client.get_stress_daily(
        start_date=args.start_date,
        end_date=args.end_date,
    ))


def _setup_wellness_hrv(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("hrv", help="Get nightly HRV readings and baseline (garth: hrv-service)")
    p.add_argument("--date", required=True, help="Date, YYYY-MM-DD")
    p.set_defaults(func=lambda client, args: client.get_hrv(
        date=args.date,
    ))


def _setup_wellness_weight(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("weight", help="Get weight entries for a date range (garth: weight-service)")
    p.add_argument("--start-date", required=True, help="Start date, YYYY-MM-DD")
    p.add_argument("--end-date", required=True, help="End date, YYYY-MM-DD")
    p.set_defaults(func=lambda client, args: client.get_weight(
        start_date=args.start_date,
        end_date=args.end_date,
    ))


def _setup_wellness_training_readiness(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("training-readiness", help="Get training readiness score (garth: metrics-service)")
    p.add_argument("--date", required=True, help="Date, YYYY-MM-DD")
    p.set_defaults(func=lambda client, args: client.get_training_readiness(
        date=args.date,
    ))


def _setup_wellness_training_status(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("training-status", help="Get training status and load (garth: mobile-gateway)")
    p.add_argument("--date", required=True, help="Date, YYYY-MM-DD")
    p.set_defaults(func=lambda client, args: client.get_training_status(
        date=args.date,
    ))


def _setup_calendar_note(subparser: argparse._SubParsersAction) -> None:
    p = subparser.add_parser("note", help="Get full content of a calendar note (API 8)")
    p.add_argument("--note-id", type=int, required=True, help="Note ID from calendar item")
    p.set_defaults(func=lambda client, args: client.get_note(
        note_id=args.note_id,
    ))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="garmin_cli.py",
        description="Garmin Connect CLI — access Garmin Connect APIs and output raw JSON.",
    )
    parser.add_argument("--cookie", help="Cookie header value (overrides GARMIN_COOKIE env var)")
    parser.add_argument("--csrf-token", help="CSRF token value (overrides GARMIN_CSRF_TOKEN env var)")
    # Note: --output is intentionally on the root parser so it can be used with any
    # subcommand. However, argparse requires global flags to appear BEFORE the subcommand.
    # Example: garmin_cli.py --output file.json activities search --limit 5 --start 0
    parser.add_argument("--output", help="Write JSON output to a file instead of stdout (must appear before subcommand)")

    subparsers = parser.add_subparsers(dest="command", help="API command group")

    # activities
    activities_parser = subparsers.add_parser("activities", help="Activity APIs")
    activities_sub = activities_parser.add_subparsers(dest="subcommand", help="Activity subcommand")
    _setup_activities_search(activities_sub)
    _setup_activities_detail(activities_sub)
    _setup_activities_download(activities_sub)
    _setup_activities_gear(activities_sub)

    # metrics
    metrics_parser = subparsers.add_parser("metrics", help="Metrics APIs (hill score, endurance score)")
    metrics_sub = metrics_parser.add_subparsers(dest="subcommand", help="Metrics subcommand")
    _setup_metrics_hill_score(metrics_sub)
    _setup_metrics_endurance_score(metrics_sub)

    # sleep
    sleep_parser = subparsers.add_parser("sleep", help="Sleep APIs")
    sleep_sub = sleep_parser.add_subparsers(dest="subcommand", help="Sleep subcommand")
    _setup_sleep_stats(sleep_sub)
    _setup_sleep_detail(sleep_sub)

    # wellness
    wellness_parser = subparsers.add_parser("wellness", help="Wellness APIs (stress, body battery, etc.)")
    wellness_sub = wellness_parser.add_subparsers(dest="subcommand", help="Wellness subcommand")
    _setup_wellness_stress_weekly(wellness_sub)
    _setup_wellness_stress_daily(wellness_sub)
    _setup_wellness_hrv(wellness_sub)
    _setup_wellness_weight(wellness_sub)
    _setup_wellness_training_readiness(wellness_sub)
    _setup_wellness_training_status(wellness_sub)

    # calendar
    calendar_parser = subparsers.add_parser("calendar", help="Calendar APIs")
    calendar_sub = calendar_parser.add_subparsers(dest="subcommand", help="Calendar subcommand")
    _setup_calendar_month(calendar_sub)
    _setup_calendar_note(calendar_sub)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if not args.subcommand:
        # Print help for the command group
        parser.parse_args([args.command, "--help"])

    # Resolve auth: CLI flags > env vars > OAuth tokens
    cookie = args.cookie or os.environ.get("GARMIN_COOKIE")
    csrf_token = args.csrf_token or os.environ.get("GARMIN_CSRF_TOKEN")

    if cookie:
        client = GarminClient(cookie=cookie, csrf_token=csrf_token)
    else:
        # Try OAuth tokens from ~/.garmin_tokens/
        from garmin_auth import load_tokens
        tokens = load_tokens()
        if tokens:
            oauth1, oauth2 = tokens
            client = GarminClient(oauth1_token=oauth1, oauth2_token=oauth2)
        else:
            print(
                "Error: No credentials found. Either:\n"
                "  1. Run: python garmin_auth.py  (log in with email/password)\n"
                "  2. Set GARMIN_COOKIE + GARMIN_CSRF_TOKEN env vars\n"
                "  3. Use --cookie + --csrf-token flags",
                file=sys.stderr,
            )
            sys.exit(1)

    try:
        result = args.func(client, args)
    except requests.HTTPError as e:
        print(f"Error: HTTP {e.response.status_code} — {e.response.text[:500]}", file=sys.stderr)
        sys.exit(1)

    # Binary download commands return a file path string, not JSON
    if isinstance(result, str):
        print(f"Saved: {result}", file=sys.stderr)
        return

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
            f.write("\n")
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
