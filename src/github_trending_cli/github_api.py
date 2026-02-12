import requests
from .errors import GitHubAPIError
import os


GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"


# send search query for repos
def search_query_from(query: str, limit: int, *, token: str | None = None ) -> list[dict]:
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
        resp = requests.get(url=GITHUB_SEARCH_URL, params=params, headers=headers, timeout=15)

    except requests.RequestException as e:
        raise GitHubAPIError(f"Network error: {e}") from e

    if resp.status_code != 200:
        try:
            msg = resp.json().get("message", "")
        except Exception:
            msg = resp.text[:200]
        raise GitHubAPIError(f"Github API error {resp.status_code}: {msg}")

    data = resp.json()
    items = data.get("items", [])
    return items[:limit]
