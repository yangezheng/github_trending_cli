
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

from .errors import (
    GitHubApiError,
    InvalidDurationError,
    InvalidLimitError,
    NetworkError,
    ParseError,
)


DURATION_TO_DAYS: dict[str, int] = {
    "day": 1,
    "week": 7,
    "month": 30,
    "year": 365,
}

GITHUB_SEARCH_REPOS_URL = "https://api.github.com/search/repositories"


@dataclass(frozen=True)
class Repo:
    full_name: str
    html_url: str
    description: str
    stargazers_count: int
    language: str


def _validate_duration(duration: str) -> str:
    duration = (duration or "").strip().lower()
    if duration not in DURATION_TO_DAYS:
        raise InvalidDurationError(duration)
    return duration


def _validate_limit(limit: int) -> int:
    if not isinstance(limit, int):
        raise InvalidLimitError(limit)
    if limit < 1 or limit > 100:
        raise InvalidLimitError(limit)
    return limit


def duration_to_since_date(duration: str) -> str:
    """
    Convert duration (day/week/month/year) into an ISO date string (YYYY-MM-DD)
    representing the earliest 'created' date to include.
    """
    duration = _validate_duration(duration)
    days = DURATION_TO_DAYS[duration]
    since = datetime.now(timezone.utc) - timedelta(days=days)
    return since.date().isoformat()


def fetch_trending_repos(duration: str = "week", limit: int = 10) -> list[Repo]:
    """
    Fetch trending repositories created within the last {duration} and sorted by stars desc.
    Uses GitHub Search API (public, no auth).
    """
    duration = _validate_duration(duration)
    limit = _validate_limit(limit)

    since_date = duration_to_since_date(duration)
    q = f"created:>={since_date}"

    # GitHub Search API supports up to 100 per_page
    params = {
        "q": q,
        "sort": "stars",
        "order": "desc",
        "per_page": str(limit),
        "page": "1",
    }

    headers = {
        "Accept": "application/vnd.github+json",
        # Setting a UA avoids some edge-case blocks and is generally good practice.
        "User-Agent": "github-trending-cli",
    }

    try:
        resp = requests.get(GITHUB_SEARCH_REPOS_URL, params=params, headers=headers, timeout=15)
    except requests.RequestException as e:
        raise NetworkError(f"Network error while calling GitHub API: {e}") from e

    # Handle non-2xx
    if resp.status_code < 200 or resp.status_code >= 300:
        # Try to extract message from GitHub response
        msg = resp.text
        try:
            data = resp.json()
            if isinstance(data, dict) and "message" in data:
                msg = data["message"]
        except Exception:
            pass

        # Rate limit is common without auth
        if resp.status_code == 403 and "rate limit" in msg.lower():
            msg = (
                f"{msg} (Unauthenticated requests are rate-limited. "
                f"Try again later.)"
            )

        raise GitHubApiError(resp.status_code, msg)

    try:
        payload: Any = resp.json()
    except ValueError as e:
        raise ParseError("Failed to parse JSON response from GitHub API.") from e

    if not isinstance(payload, dict) or "items" not in payload or not isinstance(payload["items"], list):
        raise ParseError("Unexpected JSON structure from GitHub API.")

    repos: list[Repo] = []
    for item in payload["items"]:
        if not isinstance(item, dict):
            continue
        repos.append(
            Repo(
                full_name=str(item.get("full_name", "")),
                html_url=str(item.get("html_url", "")),
                description=(item.get("description") or "").strip(),
                stargazers_count=int(item.get("stargazers_count", 0) or 0),
                language=str(item.get("language") or ""),
            )
        )

    # Sort defensively (even though API sorted), then trim to limit
    repos.sort(key=lambda r: r.stargazers_count, reverse=True)
    return repos[:limit]
