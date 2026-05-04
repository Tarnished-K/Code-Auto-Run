from datetime import datetime
from zoneinfo import ZoneInfo

from src.runtime_window_guard import RuntimeWindow


def at(hour: int, minute: int) -> datetime:
    return datetime(2026, 5, 4, hour, minute, tzinfo=ZoneInfo("Asia/Tokyo"))


def test_0359_jst_is_not_allowed() -> None:
    assert not RuntimeWindow().is_allowed(at(3, 59))


def test_0400_jst_is_allowed() -> None:
    assert RuntimeWindow().is_allowed(at(4, 0))


def test_0649_jst_can_start_new_article() -> None:
    assert RuntimeWindow().can_start_new_article(at(6, 49))


def test_0650_jst_cannot_start_new_article() -> None:
    assert not RuntimeWindow().can_start_new_article(at(6, 50))


def test_0700_jst_is_not_allowed() -> None:
    assert not RuntimeWindow().is_allowed(at(7, 0))
