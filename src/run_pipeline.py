from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from src.article_format import ArticleDraft, validate_article_format
from src.article_generator import ArticleGenerationRequest, DEFAULT_OPENAI_MODEL, generate_article_body
from src.duplicate_checker import build_fingerprint, is_duplicate
from src.env_loader import load_dotenv
from src.google_drive_client import GoogleDriveDocsClient
from src.ledger import LedgerEntry, append_ledger_entry
from src.risk_checker import assess_risk
from src.runtime_window_guard import RuntimeWindow


def main(test_run: bool = False) -> int:
    load_dotenv()
    window = RuntimeWindow()
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    if not test_run and not window.is_allowed(now):
        _log_run("outside runtime window; normal execution skipped")
        return 0
    if not test_run and not window.can_start_new_article(now):
        _log_run("hard stop reached; new article skipped")
        return 0

    title = "CodexでGoogle Docs記事在庫を作る実験ログ"
    genre_key = "ai_agents_automation_logs"
    fingerprint = build_fingerprint(
        genre_key=genre_key,
        title=title,
        main_keywords=("Codex", "Google Docs", "記事在庫"),
        source_urls=("https://developers.openai.com/codex/guides/agents-md",),
    )
    ledger_path = Path("data/article_ledger.json")
    if is_duplicate(fingerprint, ledger_path):
        _log_run(f"duplicate skipped: {fingerprint}")
        return 0

    draft = ArticleDraft(
        title=title,
        genre="01_AIエージェント_自動化_実験ログ",
        source_urls=("https://developers.openai.com/codex/guides/agents-md",),
        fingerprint=fingerprint,
    )
    body = generate_article_body(
        ArticleGenerationRequest(
            draft=draft,
            model=os.environ.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL),
        )
    )
    errors = validate_article_format(body)
    risk = assess_risk(body)
    if errors or risk.status != "stock_draft":
        _log_run(f"article blocked: errors={errors}, risk={risk}")
        return 1

    client = GoogleDriveDocsClient.from_env(dry_run=True if test_run else None)
    result = client.save_document(
        title=f"{now.date().isoformat()}__01__{title}__stock_draft",
        body=body,
        folder_name=draft.genre,
    )
    append_ledger_entry(
        ledger_path,
        LedgerEntry(
            article_id=f"{now.date().isoformat()}-ai-agents-001",
            title=title,
            genre_key=genre_key,
            status="stock_draft",
            created_at=now.isoformat(),
            drive_folder_id=result.folder_id,
            google_doc_id=result.document_id,
            google_doc_url=result.document_url,
            fingerprint=fingerprint,
            quality_score=80,
            risk_level=risk.level,
            source_urls=list(draft.source_urls),
            youtube_video_ids=list(draft.youtube_video_ids),
            estimated_price_jpy=1480,
        ),
    )
    mode = "test dry-run" if test_run else ("dry-run" if result.dry_run else "live")
    _log_run(f"{mode} article saved: {result.document_id}")
    return 0


def _log_run(message: str) -> None:
    path = Path("logs/runs/run.log")
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{timestamp} {message}\n")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the article stock pipeline.")
    parser.add_argument(
        "--test-run",
        action="store_true",
        help="Run one dry-run article outside the runtime window for local verification.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    raise SystemExit(main(test_run=args.test_run))
