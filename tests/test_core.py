from datetime import date
import pytest

from github_trending_cli.errors import InvalidDurationError
from github_trending_cli.core import parse_duration, build_query, since_date


def test_parse_duration_valid():
    assert parse_duration("1w") == 7
    assert parse_duration("1m") == 30
    assert parse_duration("1y") == 365


def test_parse_duration_invalid():
    with pytest.raises(InvalidDurationError):
        parse_duration("2w")


def test_since_date():
    today = date(2026, 2, 10)
    assert since_date(days=7, today=today) == date(2026, 2, 3).isoformat()


def test_today():
    assert since_date(days=0) == date.today().isoformat()


def test_build_query():
    assert build_query("2026-02-01") == "created:>=2026-02-01"
