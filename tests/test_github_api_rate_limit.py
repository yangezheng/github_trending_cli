import pytest

from github_trending_cli.errors import GitHubAPIError
import github_trending_cli.github_api as ghapi


class DummyResp:
    def __init__(self, status_code, json_data=None, text="", headers=None):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text
        self.headers = headers or {}

    def json(self):
        if self._json_data is None:
            raise ValueError("no json")
        return self._json_data


def test_rate_limit_hint_in_error(monkeypatch):
    def fake_get(url, params=None, headers=None, timeout=None):
        return DummyResp(
            403,
            json_data={"message": "API rate limit exceeded"},
            headers={
                "X-RateLimit-Limit": "60",
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": "1739451234",
            },
        )

    monkeypatch.setattr(ghapi.requests, "get", fake_get)

    with pytest.raises(GitHubAPIError) as e:
        ghapi.search_query_from("created:>=2026-01-01", 10)

    msg = str(e.value)
    assert "403" in msg
    assert "rate limit" in msg.lower()
    assert "remaining=0/60" in msg
    assert "resets_at_unix=1739451234" in msg


def test_token_is_added_to_headers(monkeypatch):
    captured = {}

    def fake_get(url, params=None, headers=None, timeout=None):
        captured["headers"] = headers
        return DummyResp(200, json_data={"items": []})

    monkeypatch.setattr(ghapi.requests, "get", fake_get)

    ghapi.search_query_from("created:>=2026-01-01", 10, token="TEST_TOKEN")

    assert "Authorization" in captured["headers"]
    assert captured["headers"]["Authorization"].startswith("Bearer ")
