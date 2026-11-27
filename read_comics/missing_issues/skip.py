from calendar import monthrange
from datetime import date, timedelta

SKIP_DURATIONS = {
    "7d": ("7 days", timedelta(days=7)),
    "30d": ("30 days", timedelta(days=30)),
    "6m": ("6 months", 6),
    "1y": ("1 year", 12),
}


def get_skip_until(duration: str, today: date) -> date:
    _, interval = SKIP_DURATIONS[duration]
    if isinstance(interval, timedelta):
        return today + interval

    years, month_index = divmod(today.month - 1 + interval, 12)
    year, month = today.year + years, month_index + 1
    return date(year, month, min(today.day, monthrange(year, month)[1]))
