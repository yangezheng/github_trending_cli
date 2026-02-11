

class TrendingReposError(Exception):
    """Base error for this project."""



class InvalidDurationError(TrendingReposError):
    def __init__(self, duration: str):
        super().__init__(
            f"Invalid --duration '{duration}'. Must be one of: day, week, month, year."
        )


class InvalidLimitError(TrendingReposError):
    def __init__(self, limit: int):
        super().__init__(
            f"Invalid --limit '{limit}'. Must be an integer between 1 and 100."
        )


class NetworkError(TrendingReposError):
    def __init__(self, message: str):
        super().__init__(message)


class ParseError(TrendingReposError):
    def __init__(self, message: str):
        super().__init__(message)


class GitHubApiError(TrendingReposError):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"GitHub API error ({status_code}): {message}")
