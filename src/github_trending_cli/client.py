from .core import parse_duration, since_date, build_query
from .github_api import search_query_from
from .models import Repo, repo_from_api


def trending(duration: str = '1w', limit: int = 10) -> list[Repo]:
    # return a list of repos
    days = parse_duration(duration)
    since = since_date(days)
    query = build_query(since)

    items = search_query_from(query, limit)
    return [repo_from_api(item) for item in items]