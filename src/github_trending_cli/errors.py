# errors.py
class GHTTrendingError(Exception):
    """Base error for ghtrending."""


class InvalidDurationError(GHTTrendingError):
    "invalid duration"


class InvalidLimitError(GHTTrendingError):
    "invalid limit"


class GitHubAPIError(GHTTrendingError):
    "github api requests fail"
