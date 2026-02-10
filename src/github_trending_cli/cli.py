from __future__ import annotations

import argparse
import sys
from textwrap import shorten

from .core import fetch_trending_repos
from .errors import (
    GitHubApiError,
    InvalidDurationError,
    InvalidLimitError,
    NetworkError,
    ParseError,
    TrendingReposError,
)


def _format_table(rows: list[dict]) -> str:
    """
    Simple monospace table formatter (no external deps).
    """
    headers = ["#", "Repository", "Stars", "Language", "Description"]
    cols = [
        [str(r["idx"]) for r in rows],
        [r["name"] for r in rows],
        [str(r["stars"]) for r in rows],
        [r["lang"] for r in rows],
        [r["desc"] for r in rows],
    ]

    widths = [len(h) for h in headers]
    for i, col in enumerate(cols):
        widths[i] = max(widths[i], max((len(x) for x in col), default=0))

    def line(parts: list[str]) -> str:
        return "  ".join(p.ljust(widths[i]) for i, p in enumerate(parts))

    out = [line(headers), line(["-" * w for w in widths])]
    for r in rows:
        out.append(
            line(
                [
                    str(r["idx"]),
                    r["name"],
                    str(r["stars"]),
                    r["lang"],
                    r["desc"],
                ]
            )
        )
    return "\n".join(out)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="trending-repos",
        description="Show trending GitHub repositories by stars over a time window.",
    )
    parser.add_argument(
        "--duration",
        default="week",
        choices=["day", "week", "month", "year"],
        help="Time window for trending repositories (default: week).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of repositories to display (1-100, default: 10).",
    )

    args = parser.parse_args(argv)

    try:
        repos = fetch_trending_repos(duration=args.duration, limit=args.limit)

        rows = []
        for i, r in enumerate(repos, start=1):
            rows.append(
                {
                    "idx": i,
                    "name": r.full_name,
                    "stars": r.stargazers_count,
                    "lang": r.language or "-",
                    "desc": shorten(r.description or "-", width=80, placeholder="…"),
                }
            )

        if not rows:
            print("No repositories found for the given duration.")
            return

        print(_format_table(rows))
        print("\nLinks:")
        for r in repos:
            print(f"- {r.full_name}: {r.html_url}")

    except (InvalidDurationError, InvalidLimitError) as e:
        print(f"Input error: {e}", file=sys.stderr)
        sys.exit(2)
    except (NetworkError, ParseError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except GitHubApiError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except TrendingReposError as e:
        # Catch-all for project-defined errors
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
