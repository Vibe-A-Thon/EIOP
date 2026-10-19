"""Time utilities for RFC 3339 UTC timestamps with millisecond precision (T-103)."""

from __future__ import annotations

import re
from datetime import datetime, timezone

TS_PATTERN = re.compile(r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,6}))?Z$")


def utc_now_ms() -> datetime:
    """Return current UTC datetime truncated to milliseconds."""
    dt = datetime.now(timezone.utc)
    # Truncate microsecond to millisecond
    ms = (dt.microsecond // 1000) * 1000
    return dt.replace(microsecond=ms)


def format_ts(dt: datetime) -> str:
    """Format datetime as strict RFC 3339 UTC string with millisecond precision and Z suffix."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    ms = dt.microsecond // 1000
    return dt.strftime(f"%Y-%m-%dT%H:%M:%S.{ms:03d}Z")


def parse_ts(s: str) -> datetime:
    """Parse strict RFC 3339 UTC string with Z suffix into datetime, or raise ValueError."""
    m = TS_PATTERN.match(s)
    if not m:
        raise ValueError(f"Invalid timestamp '{s}': expected RFC 3339 UTC with 'Z' suffix and millisecond precision")

    year, month, day, hour, minute, second = map(int, m.groups()[:6])
    frac_str = m.group(7) or "0"
    # Pad or truncate fraction to 6 digits (microseconds)
    microsecond = int(frac_str.ljust(6, "0")[:6])

    return datetime(
        year, month, day, hour, minute, second, microsecond=microsecond, tzinfo=timezone.utc
    )
