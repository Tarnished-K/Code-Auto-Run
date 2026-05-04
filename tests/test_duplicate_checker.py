import json

from src.duplicate_checker import build_fingerprint, is_duplicate


def test_same_video_and_title_is_duplicate(tmp_path) -> None:
    fingerprint = build_fingerprint("genre", "同じタイトル", ["abc"], ["keyword"], ["https://example.com"])
    ledger = tmp_path / "ledger.json"
    ledger.write_text(json.dumps([{"fingerprint": fingerprint}]), encoding="utf-8")
    assert is_duplicate(fingerprint, ledger)


def test_different_genre_changes_fingerprint() -> None:
    first = build_fingerprint("genre-a", "同じタイトル", ["abc"])
    second = build_fingerprint("genre-b", "同じタイトル", ["abc"])
    assert first != second
