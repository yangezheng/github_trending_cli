from .errors import InvalidDurationError
from datetime import date, timedelta
_ALLOWED = {
    '1w': 7,
    '1m': 30,
    '3m': 90,
    '6m': 180,
    '1y': 365,
}

# parse duration to number of days
# e.g. 1 week -> 7
def parse_duration(duration_str) -> int:
    if duration_str not in _ALLOWED:
        raise InvalidDurationError(f"duration must be one of".join(_ALLOWED))
    return _ALLOWED[duration_str]


# build since YYYY-MM-DD
# from days 
def since_date(days: int, today: date | None = None) -> str:
    today = today or date.today()
    since_date = today-timedelta(days = days)
    return since_date.isoformat()


# build query
def build_query(since_date: str) -> str:
    return f"created:>={since_date}"