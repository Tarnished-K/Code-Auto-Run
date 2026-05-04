import json

from src.google_drive_client import GoogleDriveDocsClient, _escape_query_value


def test_dry_run_writes_pending_payload(tmp_path) -> None:
    client = GoogleDriveDocsClient(dry_run=True, pending_dir=tmp_path)
    result = client.save_document("title", "body", "folder")
    payload_path = tmp_path / f"{result.document_id}.json"

    assert result.dry_run
    assert payload_path.exists()
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    assert payload["title"] == "title"
    assert payload["body"] == "body"
    assert payload["folder_name"] == "folder"


def test_drive_query_value_escaping() -> None:
    assert _escape_query_value("owner's folder") == "owner\\'s folder"
