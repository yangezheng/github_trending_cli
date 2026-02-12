import argparse
from .core import parse_duration,since_date, build_query
from .github_api import search_query_from
from .errors import InvalidDurationError, InvalidLimitError, GitHubAPIError

def main():
    parser = argparse.ArgumentParser(description="GitHub Trending CLI, use this library to retrieve the most stared repos for the last period of time")
    parser.add_argument("-d" , "--duration", default='1w', help="To get the last period of repos, valid args: [1w, 1m, 3m, 6m, 1y], default is '1w'")
    parser.add_argument('-l',"--limit", type = int, default=10, help="set the number of repos you want to retrieve")
    args = parser.parse_args()

    try:
        days = parse_duration(args.duration)
        since = since_date(days)
        query = build_query(since)

        repos = search_query_from(query=query, limit = args.limit)

        for repo in repos:
            print(f"{repo['full_name']} with {repo['stargazers_count']} stars")
        
    except InvalidDurationError as e:
        print(f"Error: {e}")
    except GitHubAPIError as e:
        print(f"API Error: {e}")
    
if __name__ == "__main__":
    main()
