# errors.py
class GHTTrendingError(Exception):
    """Base error for ghtrending."""


class InvalidDurationError(GHTTrendingError):
    pass


class InvalidLimitError(GHTTrendingError):
    pass


class GitHubAPIError(GHTTrendingError):
    pass
