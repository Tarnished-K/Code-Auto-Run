import json

from src import run_pipeline


def test_test_run_forces_dry_run_and_writes_ledger(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert run_pipeline.main(test_run=True) == 0

    ledger = json.loads((tmp_path / "data" / "article_ledger.json").read_text(encoding="utf-8"))
    assert len(ledger) == 1
    assert ledger[0]["google_doc_url"].startswith("dry-run://")
    assert list((tmp_path / "outputs" / "pending_drive").glob("*.json"))
