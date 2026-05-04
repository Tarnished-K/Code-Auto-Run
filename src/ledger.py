from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class LedgerEntry:
    article_id: str
    title: str
    genre_key: str
    status: str
    created_at: str
    drive_folder_id: str
    google_doc_id: str
    google_doc_url: str
    fingerprint: str
    quality_score: int
    risk_level: str
    source_urls: list[str]
    youtube_video_ids: list[str]
    estimated_price_jpy: int


def append_ledger_entry(path: str | Path, entry: LedgerEntry) -> None:
    ledger_path = Path(path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    entries = []
    if ledger_path.exists():
        entries = json.loads(ledger_path.read_text(encoding="utf-8") or "[]")
    entries.append(asdict(entry))
    ledger_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
