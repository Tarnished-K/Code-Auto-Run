from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class RuntimeWindow:
    timezone: str = "Asia/Tokyo"
    start: str = "04:00"
    end: str = "07:00"
    hard_stop_new_tasks: str = "06:50"
    allow_manual_run_outside_window: bool = False

    def is_allowed(self, now: datetime | None = None, manual: bool = False) -> bool:
        local_now = self._localize(now)
        if manual and self.allow_manual_run_outside_window:
            return True
        return _parse_time(self.start) <= local_now.time() < _parse_time(self.end)

    def can_start_new_article(self, now: datetime | None = None, manual: bool = False) -> bool:
        local_now = self._localize(now)
        if not self.is_allowed(local_now, manual=manual):
            return False
        return local_now.time() < _parse_time(self.hard_stop_new_tasks)

    def _localize(self, now: datetime | None) -> datetime:
        zone = ZoneInfo(self.timezone)
        if now is None:
            return datetime.now(zone)
        if now.tzinfo is None:
            return now.replace(tzinfo=zone)
        return now.astimezone(zone)


def _parse_time(value: str) -> time:
    hour, minute = value.split(":", maxsplit=1)
    return time(hour=int(hour), minute=int(minute))
