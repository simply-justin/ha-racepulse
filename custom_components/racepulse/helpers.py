from datetime import datetime, timedelta
from typing import Any, Optional


@staticmethod
def parse_int(value: Any) -> int:
    """Convert value to int, returning 0 on error."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

@staticmethod
def parse_string(value: Any) -> str:
    """Convert a value to a string, returning an empty string for None."""
    return str(value) if value is not None else ""

@staticmethod
def parse_bool(value: Any) -> bool:
    """
    Convert a value to a boolean.

    Accepts common truthy strings like 'true', '1', 'yes'.
    Returns False for None, '', or other unrecognized values.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return bool(value)

@staticmethod
def parse_float(value: Any) -> float:
    """Convert a value to float, returning 0.0 on error."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

@staticmethod
def parse_datetime(value: Optional[str]) -> Optional[datetime]:
    """
    Parse an ISO 8601 datetime string (e.g., '2025-10-03T15:37:14.4783763Z').

    Returns None on invalid or missing input.
    """
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None

@staticmethod
def parse_timedelta(value: Optional[str]) -> timedelta:
    """
    Parse a string formatted as 'HH:MM:SS' into a timedelta.

    Returns timedelta(0) on invalid or missing input.
    """
    if not value:
        return timedelta()
    try:
        hours, minutes, seconds = map(int, value.split(":"))
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    except (ValueError, TypeError):
        return timedelta()
