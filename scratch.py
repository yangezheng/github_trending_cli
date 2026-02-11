from src.github_trending_cli.core import since_date, build_query
from src.github_trending_cli.github_api import search_query_from

since = since_date(7)
q = build_query(since)

items = search_query_from(q,5)
print("count:", len(items))
for r in items:
    print(r["full_name"], r["stargazers_count"])