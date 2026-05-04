from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


def normalize_title(title: str) -> str:
    lowered = title.casefold()
    return re.sub(r"\W+", "", lowered)


def build_fingerprint(
    genre_key: str,
    title: str,
    youtube_video_ids: list[str] | tuple[str, ...] = (),
    main_keywords: list[str] | tuple[str, ...] = (),
    source_urls: list[str] | tuple[str, ...] = (),
) -> str:
    payload = {
        "genre_key": genre_key,
        "normalized_title": normalize_title(title),
        "youtube_video_ids": sorted(youtube_video_ids),
        "main_keywords": sorted(keyword.casefold() for keyword in main_keywords),
        "source_urls": sorted(source_urls),
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def is_duplicate(fingerprint: str, ledger_path: str | Path) -> bool:
    path = Path(ledger_path)
    if not path.exists():
        return False
    entries = json.loads(path.read_text(encoding="utf-8") or "[]")
    return any(entry.get("fingerprint") == fingerprint for entry in entries)
