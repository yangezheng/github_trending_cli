import github_trending_cli.client as client


def test_trending_calls_api_and_maps(monkeypatch):
    # define fake search
    def fake_search_query_from(query: str, limit: int):
        assert "created:>=" in query
        assert limit == 2

        return [
            {
                "full_name": "a/b",
                "stargazers_count": 10,
                "html_url": "https://github.com/a/b",
                "description": "hello",
                "language": "Python",
            },
            {
                "full_name": "c/d",
                "stargazers_count": 9,
                "html_url": "https://github.com/c/d",
                "description": None,
                "language": None,
            },
        ]

    # substitute fake search
    monkeypatch.setattr(client, "search_query_from", fake_search_query_from)

    repos = client.trending("1w", 2)

    assert len(repos) == 2
    assert repos[0].full_name == "a/b"
    assert repos[0].stars == 10
    assert repos[0].url == "https://github.com/a/b"
    assert repos[0].language == "Python"

    assert repos[1].full_name == "c/d"
    assert repos[1].stars == 9
    assert repos[1].description is None
