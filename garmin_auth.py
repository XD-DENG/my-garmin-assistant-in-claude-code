#!/usr/bin/env python3
"""
Garmin Connect Auth — Log in via Garmin SSO and save OAuth tokens.

Mimics the Garmin Connect Mobile app's login flow:
  1. POST email+password to sso.garmin.com → get a login ticket
  2. Exchange ticket for an OAuth1 token (~1 year lifespan)
  3. Exchange OAuth1 for an OAuth2 access token (auto-refreshable)

Your credentials are sent ONLY to sso.garmin.com (Garmin's own SSO server).
Tokens are saved as plain JSON in ~/.garmin_tokens/.

Usage:
    pip install requests requests-oauthlib
    python garmin_auth.py

Dependencies: requests, requests-oauthlib
"""

from __future__ import annotations

import getpass
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import parse_qs

import requests
from requests_oauthlib import OAuth1Session

# ── Constants ────────────────────────────────────────────────────────────

DOMAIN = "garmin.com"
SSO = f"https://sso.{DOMAIN}/sso"
SSO_EMBED = f"{SSO}/embed"
CONNECT_API = f"https://connectapi.{DOMAIN}"
USER_AGENT = "com.garmin.android.apps.connectmobile"
TOKEN_DIR = Path.home() / ".garmin_tokens"

# OAuth consumer credentials (same as the official Garmin Connect Mobile app).
# Hardcoded for simplicity; falls back to fetching from S3 if these fail.
CONSUMER_KEY = "fc3e99d2-118c-44b8-8ae3-03370dde24c0"
CONSUMER_SECRET = "E08WAR897WEy2knn7aFBrvegVAf0AFdWBBF"


# ── SSO Login (steps 1-3) ────────────────────────────────────────────────

def login(email: str, password: str) -> str:
    """Log into Garmin SSO and return a login ticket.

    Sends 3 HTTP requests to sso.garmin.com:
      1. GET /sso/embed — establish session cookies
      2. GET /sso/signin — get CSRF token from HTML form
      3. POST /sso/signin — submit email + password

    Returns:
        A ticket string used to obtain OAuth tokens.
    """
    sess = requests.Session()
    sess.headers["User-Agent"] = USER_AGENT

    embed_params = {
        "id": "gauth-widget",
        "embedWidget": "true",
        "gauthHost": SSO,
    }
    signin_params = {
        **embed_params,
        "gauthHost": SSO_EMBED,
        "service": SSO_EMBED,
        "source": SSO_EMBED,
        "redirectAfterAccountLoginUrl": SSO_EMBED,
        "redirectAfterAccountCreationUrl": SSO_EMBED,
    }

    # Step 1: Set session cookies
    sess.get(f"{SSO}/embed", params=embed_params)

    # Step 2: Get CSRF token from signin page
    resp = sess.get(f"{SSO}/signin", params=signin_params)
    csrf_match = re.search(r'name="_csrf"\s+value="(.+?)"', resp.text)
    if not csrf_match:
        raise RuntimeError("Could not find CSRF token on login page")
    csrf_token = csrf_match.group(1)

    # Step 3: Submit login form
    resp = sess.post(
        f"{SSO}/signin",
        params=signin_params,
        headers={"Referer": resp.url},
        data={
            "username": email,
            "password": password,
            "embed": "true",
            "_csrf": csrf_token,
        },
    )

    # Handle MFA if needed
    title_match = re.search(r"<title>(.+?)</title>", resp.text)
    title = title_match.group(1) if title_match else ""

    if "MFA" in title:
        csrf_match = re.search(r'name="_csrf"\s+value="(.+?)"', resp.text)
        csrf_token = csrf_match.group(1) if csrf_match else csrf_token
        mfa_code = input("MFA code: ")
        resp = sess.post(
            f"{SSO}/verifyMFA/loginEnterMfaCode",
            params=signin_params,
            headers={"Referer": resp.url},
            data={
                "mfa-code": mfa_code,
                "embed": "true",
                "_csrf": csrf_token,
                "fromPage": "setupEnterMfaCode",
            },
        )
        title_match = re.search(r"<title>(.+?)</title>", resp.text)
        title = title_match.group(1) if title_match else ""

    if title != "Success":
        raise RuntimeError(
            f"Login failed (page title: '{title}'). "
            "Check your email/password."
        )

    # Parse ticket from success page
    ticket_match = re.search(r'embed\?ticket=([^"]+)"', resp.text)
    if not ticket_match:
        raise RuntimeError("Login succeeded but could not find ticket")
    return ticket_match.group(1)


# ── OAuth token exchange (steps 4-5) ─────────────────────────────────────

def get_consumer_credentials() -> tuple[str, str]:
    """Return OAuth consumer key and secret.

    Uses hardcoded values; falls back to fetching from S3 if they fail.
    """
    return CONSUMER_KEY, CONSUMER_SECRET


def fetch_consumer_credentials_from_s3() -> tuple[str, str]:
    """Fetch OAuth consumer credentials from garth's S3 bucket.

    NOTE: This contacts thegarth.s3.amazonaws.com, which is controlled by the
    garth library author (not Garmin). This is only called if the hardcoded
    consumer keys fail (e.g. Garmin rotated them). The keys are only used for
    OAuth1 request signing against Garmin's server — a compromised key would
    cause auth to fail, not leak your credentials.
    """
    resp = requests.get(
        "https://thegarth.s3.amazonaws.com/oauth_consumer.json"
    )
    data = resp.json()
    return data["consumer_key"], data["consumer_secret"]


def get_oauth1_token(ticket: str) -> dict:
    """Exchange a login ticket for an OAuth1 token.

    The OAuth1 token lasts approximately 1 year.
    """
    key, secret = get_consumer_credentials()
    sess = OAuth1Session(key, secret)
    sess.headers["User-Agent"] = USER_AGENT

    resp = sess.get(
        f"{CONNECT_API}/oauth-service/oauth/preauthorized",
        params={
            "ticket": ticket,
            "login-url": f"{SSO}/embed",
            "accepts-mfa-tokens": "true",
        },
    )

    # If hardcoded keys failed, try S3 fallback
    if resp.status_code in (401, 403):
        print("Hardcoded consumer keys failed, fetching from S3...")
        key, secret = fetch_consumer_credentials_from_s3()
        sess = OAuth1Session(key, secret)
        sess.headers["User-Agent"] = USER_AGENT
        resp = sess.get(
            f"{CONNECT_API}/oauth-service/oauth/preauthorized",
            params={
                "ticket": ticket,
                "login-url": f"{SSO}/embed",
                "accepts-mfa-tokens": "true",
            },
        )

    resp.raise_for_status()
    parsed = parse_qs(resp.text)
    return {k: v[0] for k, v in parsed.items()}


def exchange_oauth2(oauth1_token: dict) -> dict:
    """Exchange an OAuth1 token for an OAuth2 access token.

    The OAuth2 token is short-lived but can be refreshed using the
    OAuth1 token (call this function again when it expires).
    """
    key, secret = get_consumer_credentials()
    sess = OAuth1Session(
        key,
        secret,
        resource_owner_key=oauth1_token["oauth_token"],
        resource_owner_secret=oauth1_token["oauth_token_secret"],
    )
    sess.headers["User-Agent"] = USER_AGENT

    resp = sess.post(
        f"{CONNECT_API}/oauth-service/oauth/exchange/user/2.0",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=(
            {"mfa_token": oauth1_token["mfa_token"]}
            if oauth1_token.get("mfa_token")
            else {}
        ),
    )
    resp.raise_for_status()

    token = resp.json()
    token["expires_at"] = int(time.time() + token["expires_in"])
    token["refresh_token_expires_at"] = int(
        time.time() + token["refresh_token_expires_in"]
    )
    return token


# ── Token storage ─────────────────────────────────────────────────────────

def save_tokens(oauth1: dict, oauth2: dict) -> None:
    """Save OAuth tokens to ~/.garmin_tokens/."""
    TOKEN_DIR.mkdir(exist_ok=True)
    os.chmod(TOKEN_DIR, 0o700)

    for name, data in [("oauth1_token", oauth1), ("oauth2_token", oauth2)]:
        path = TOKEN_DIR / f"{name}.json"
        path.write_text(json.dumps(data, indent=2) + "\n")
        os.chmod(path, 0o600)


def load_tokens() -> tuple[dict, dict] | None:
    """Load OAuth tokens from ~/.garmin_tokens/. Returns None if missing."""
    oauth1_path = TOKEN_DIR / "oauth1_token.json"
    oauth2_path = TOKEN_DIR / "oauth2_token.json"
    if not oauth1_path.exists() or not oauth2_path.exists():
        return None
    oauth1 = json.loads(oauth1_path.read_text())
    oauth2 = json.loads(oauth2_path.read_text())
    return oauth1, oauth2


# ── Main ──────────────────────────────────────────────────────────────────

def main() -> None:
    email = input("Garmin email: ")
    password = getpass.getpass("Garmin password: ")

    print("Logging in...")
    ticket = login(email, password)
    print("Login successful, exchanging tokens...")

    oauth1 = get_oauth1_token(ticket)
    oauth2 = exchange_oauth2(oauth1)

    save_tokens(oauth1, oauth2)
    print(f"Tokens saved to {TOKEN_DIR}/")
    print(
        f"OAuth1 token (login): lasts ~1 year\n"
        f"OAuth2 token (API access): expires in "
        f"{oauth2['expires_in'] // 3600}h, auto-refreshes"
    )


if __name__ == "__main__":
    main()
