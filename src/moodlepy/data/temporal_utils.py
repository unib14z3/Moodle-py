"""Helpers for converting dates to and from the configured timezone."""

from datetime import datetime, timezone

from moodlepy import config


def timestamp_to_ist(timestamp: float | None):
    """Convert a Unix timestamp to a datetime in the configured timezone."""
    if timestamp is None:
        return None

    return datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(config.IST_TZ)


def ist_to_timestamp(ist_datetime: datetime | None):
    """Convert a timezone-aware datetime to a Unix timestamp."""
    if ist_datetime is None:
        return None

    return ist_datetime.astimezone(timezone.utc).timestamp()


def str_to_ist(date_string: str | None):
    """Convert a configured date string to a timezone-aware datetime."""
    if date_string is None:
        return None

    naive_datetime = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
    return naive_datetime.replace(tzinfo=config.IST_TZ)
