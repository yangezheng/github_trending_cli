import requests
from .errors import GitHubAPIError
import os
import logging
import time

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
logger = logging.getLogger(__name__)


# send search query for repos
def search_query_from(
    query: str, limit: int, *, token: str | None = None
) -> list[dict]:
    logger.debug(
        "GitHub search start: query=%r limit=%s token=%s",
        query,
        limit,
        bool(token),
    )

    if limit <= 0:
        return []
    per_page = min(limit, 100)

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
    }

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ghtrending_CLI",
    }

    token = token or os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        start = time.perf_counter()

        resp = requests.get(
            url=GITHUB_SEARCH_URL, params=params, headers=headers, timeout=15
        )

        elapsed_ms = (time.perf_counter() - start) * 100
        logger.debug(
            "GitHub response: status=%s elapsed_ms=%.1f.",
            resp.status_code,
            elapsed_ms,
        )

    except requests.RequestException as e:
        raise GitHubAPIError(f"Network error: {e}") from e

    if resp.status_code != 200:
        logger.warning(
            "GitHub request failed with status code: (%s).",
            resp.status_code,
        )

        def _rate_limit_hint(resp: requests.Response) -> str:
            limit = resp.headers.get("X-RateLimit-Limit")
            remaining = resp.headers.get("X-RateLimit-Remaining")
            reset = resp.headers.get("X-RateLimit-Reset")

            parts = []
            if limit and remaining:
                parts.append(f"rate_limit remaining={remaining}/{limit}")
            if reset:
                parts.append(f"resets_at_unix={reset}")

            if parts:
                return " (" + ", ".join(parts) + ")"
            return ""

        try:
            msg = resp.json().get("message", "")
        except Exception:
            msg = resp.text[:200]
        hint = _rate_limit_hint(resp)
        raise GitHubAPIError(f"Github API error {resp.status_code}: {msg}{hint}")

    logger.info("Github request succeseed with status code: (%s).", resp.status_code)
    data = resp.json()
    items = data.get("items", [])
    return items[:limit]
