"""
schemas.py — L3 data structures and validation

Responsibilities:
- Date format validation
- Error type definitions
- Version number constants
"""

import re
from datetime import datetime, date

CURRENT_VERSION = "v1.0.2"


class L3Error(Exception):
    pass


class VersionError(L3Error):
    pass


class NetworkError(L3Error):
    pass


class CacheError(L3Error):
    pass


def validate_date(date_str: str) -> str | None:
    """Validate date format YYYY-MM-DD, return error message or None"""
    if not date_str:
        return None
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return f"Invalid date format, must be YYYY-MM-DD, got: {date_str}"
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return f"Invalid date: {date_str}"
    return None


def get_today() -> str:
    """Get today's date in YYYY-MM-DD format"""
    return date.today().isoformat()
