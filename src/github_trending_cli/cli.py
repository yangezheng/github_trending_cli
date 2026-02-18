import argparse
from .client import trending
from .errors import InvalidDurationError, InvalidLimitError, GitHubAPIError
import sys


def main():
    parser = argparse.ArgumentParser(
        description="GitHub Trending CLI, use this library to retrieve the most stared repos for the last period of time"
    )
    parser.add_argument(
        "-d",
        "--duration",
        default="1w",
        help="To get the last period of repos, valid args: [1w, 1m, 3m, 6m, 1y], default is '1w'",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=10,
        help="set the number of repos you want to retrieve",
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        help="Pass in the access token for GitHub API.",
    )
    args = parser.parse_args()

    try:
        repos = trending(duration=args.duration, limit=args.limit, token=args.token)
    except (InvalidDurationError, InvalidLimitError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except GitHubAPIError as e:
        print(f"API Error: {e}", file=sys.stderr)
        return 3

    for repo in repos:
        print(f"{repo.full_name} with {repo.stars} stars, at url: {repo.url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
