"""Timezone utilities with proper DST handling."""

from datetime import datetime, timezone
from typing import Optional
import pytz


class TimezoneConverter:
    """Handles timezone conversions with DST awareness."""

    VALID_TIMEZONES = set(pytz.all_timezones)

    def __init__(self, default_tz: str = "UTC"):
        self.default_tz = self._validate_timezone(default_tz)

    def _validate_timezone(self, tz_str: str) -> pytz.timezone:
        """Validate and return timezone object."""
        if tz_str not in self.VALID_TIMEZONES:
            raise ValueError(f"Invalid timezone: {tz_str}")
        return pytz.timezone(tz_str)

    def to_utc(self, dt: datetime, source_tz: Optional[str] = None) -> datetime:
        """Convert datetime to UTC."""
        if dt.tzinfo is None:
            tz = self._validate_timezone(source_tz) if source_tz else self.default_tz
            dt = tz.localize(dt)
        return dt.astimezone(pytz.UTC)

    def from_utc(self, dt: datetime, target_tz: str) -> datetime:
        """Convert UTC datetime to target timezone."""
        if dt.tzinfo is None:
            dt = pytz.UTC.localize(dt)
        target = self._validate_timezone(target_tz)
        return dt.astimezone(target)

    def convert(
        self,
        dt: datetime,
        from_tz: str,
        to_tz: str
    ) -> datetime:
        """Convert between arbitrary timezones."""
        utc_dt = self.to_utc(dt, from_tz)
        return self.from_utc(utc_dt, to_tz)

    @staticmethod
    def now_utc() -> datetime:
        """Get current UTC time."""
        return datetime.now(pytz.UTC)

    @staticmethod
    def is_dst(dt: datetime, tz_str: str) -> bool:
        """Check if datetime is in DST for given timezone."""
        tz = pytz.timezone(tz_str)
        localized = tz.localize(dt.replace(tzinfo=None))
        return bool(localized.dst())
