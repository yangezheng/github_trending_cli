 # GitHub Trending CLI

Fetch the most starred GitHub repositories created within a recent time window. Includes a CLI (`ghtrend`) and a small Python library.

## Features

- Query “trending” repositories by creation date window (1w, 1m, 3m, 6m, 1y)
- Sorts by stars (descending)
- Simple CLI output
- Reusable Python API

## Requirements

- Python 3.11+

## Install

### From source (recommended for now)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## CLI Usage

Once installed, run:

```bash
ghtrend --duration 1w --limit 10
```

### Options

- `-d`, `--duration` (default: `1w`)
	- Valid values: `1w`, `1m`, `3m`, `6m`, `1y`
- `-l`, `--limit` (default: `10`)
	- Number of repositories to return

### Example Output

```
octocat/Hello-World with 4242 stars, at url: https://github.com/octocat/Hello-World
```

## Library Usage

```python
from github_trending_cli.client import trending

repos = trending("1m", 5)
for repo in repos:
		print(repo.full_name, repo.stars, repo.url)
```

### Returned Model

`trending()` returns a list of `Repo` objects with:

- `full_name` (str)
- `stars` (int)
- `url` (str)
- `description` (str | None)
- `language` (str | None)
- `topics` (tuple[str, ...])

## Errors

The CLI exits with:

- `2` on invalid duration or limit
- `3` on GitHub API errors

In library usage, errors are raised as:

- `InvalidDurationError`
- `InvalidLimitError`
- `GitHubAPIError`

## Development

Run tests:

```bash
pytest
```

## Notes

- This uses the public GitHub Search API. Unauthenticated requests are subject to GitHub’s rate limits.

- It's initially a roadmap project: https://roadmap.sh/projects/github-trending-cli