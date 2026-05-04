from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4


DEFAULT_SCOPES = (
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/documents",
)


@dataclass(frozen=True)
class GoogleDocResult:
    document_id: str
    document_url: str
    folder_id: str
    dry_run: bool


class GoogleDriveDocsClient:
    """Google Drive/Docs writer with dry-run as the default safety mode."""

    def __init__(
        self,
        dry_run: bool = True,
        pending_dir: str | Path = "outputs/pending_drive",
        root_folder_name: str = "note記事ストック_自律生成",
        credentials_path: str | Path = "secrets/google_oauth_client.json",
        token_path: str | Path = "secrets/google_oauth_token.json",
        scopes: tuple[str, ...] = DEFAULT_SCOPES,
    ) -> None:
        self.dry_run = dry_run
        self.pending_dir = Path(pending_dir)
        self.root_folder_name = root_folder_name
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)
        self.scopes = scopes

    @classmethod
    def from_env(cls, dry_run: bool | None = None) -> GoogleDriveDocsClient:
        if dry_run is None:
            dry_run = os.environ.get("CODE_AUTO_RUN_DRY_RUN", "true").lower() != "false"
        return cls(
            dry_run=dry_run,
            root_folder_name=os.environ.get("GOOGLE_DRIVE_ROOT_FOLDER", "note記事ストック_自律生成"),
            credentials_path=os.environ.get(
                "GOOGLE_OAUTH_CLIENT_PATH",
                os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "secrets/google_oauth_client.json"),
            ),
            token_path=os.environ.get("GOOGLE_OAUTH_TOKEN_PATH", "secrets/google_oauth_token.json"),
        )

    def save_document(self, title: str, body: str, folder_name: str) -> GoogleDocResult:
        if not self.dry_run:
            return self._save_document_live(title=title, body=body, folder_name=folder_name)
        self.pending_dir.mkdir(parents=True, exist_ok=True)
        document_id = f"dryrun-{uuid4().hex}"
        folder_id = f"dryrun-folder-{folder_name}"
        payload = {
            "title": title,
            "root_folder_name": self.root_folder_name,
            "folder_name": folder_name,
            "body": body,
            "dry_run": True,
        }
        (self.pending_dir / f"{document_id}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return GoogleDocResult(
            document_id=document_id,
            document_url=f"dry-run://google-docs/{document_id}",
            folder_id=folder_id,
            dry_run=True,
        )

    def _save_document_live(self, title: str, body: str, folder_name: str) -> GoogleDocResult:
        drive_service, docs_service = self._build_services()
        root_folder_id = self._ensure_folder(drive_service, self.root_folder_name, parent_id="root")
        folder_id = self._ensure_folder(drive_service, folder_name, parent_id=root_folder_id)
        document = (
            drive_service.files()
            .create(
                body={
                    "name": title,
                    "mimeType": "application/vnd.google-apps.document",
                    "parents": [folder_id],
                },
                fields="id, webViewLink",
            )
            .execute()
        )
        document_id = document["id"]
        if body:
            docs_service.documents().batchUpdate(
                documentId=document_id,
                body={"requests": [{"insertText": {"location": {"index": 1}, "text": body}}]},
            ).execute()
        return GoogleDocResult(
            document_id=document_id,
            document_url=document.get("webViewLink", f"https://docs.google.com/document/d/{document_id}/edit"),
            folder_id=folder_id,
            dry_run=False,
        )

    def _build_services(self) -> tuple[Any, Any]:
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
        except ImportError as exc:
            raise RuntimeError(
                "Google API dependencies are missing. Run: python -m pip install -r requirements-dev.txt"
            ) from exc

        credentials = None
        if self.token_path.exists():
            credentials = Credentials.from_authorized_user_file(str(self.token_path), self.scopes)
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        if not credentials or not credentials.valid:
            if not self.credentials_path.exists():
                raise FileNotFoundError(
                    "Google OAuth client file is missing. Put it at "
                    f"{self.credentials_path} or set GOOGLE_OAUTH_CLIENT_PATH."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(self.credentials_path), self.scopes)
            credentials = flow.run_local_server(port=0)
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        self.token_path.write_text(credentials.to_json(), encoding="utf-8")
        drive_service = build("drive", "v3", credentials=credentials)
        docs_service = build("docs", "v1", credentials=credentials)
        return drive_service, docs_service

    def _ensure_folder(self, drive_service: Any, name: str, parent_id: str) -> str:
        query = (
            f"name = '{_escape_query_value(name)}' "
            "and mimeType = 'application/vnd.google-apps.folder' "
            "and trashed = false "
            f"and '{_escape_query_value(parent_id)}' in parents"
        )
        existing = (
            drive_service.files()
            .list(q=query, spaces="drive", fields="files(id, name)", pageSize=1)
            .execute()
            .get("files", [])
        )
        if existing:
            return existing[0]["id"]
        folder = (
            drive_service.files()
            .create(
                body={
                    "name": name,
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [parent_id],
                },
                fields="id",
            )
            .execute()
        )
        return folder["id"]


def _escape_query_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")
