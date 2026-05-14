"""Small shared helpers used by services and routes."""

from datetime import datetime
from decimal import Decimal
from typing import Any


def calculate_trip_duration(start_date: datetime, end_date: datetime) -> int:
    """Return inclusive trip duration in days."""
    delta = end_date.date() - start_date.date()
    return max(delta.days + 1, 1)


def json_safe(value: Any) -> Any:
    """Convert common Python objects into JSON-friendly values."""
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    return value
