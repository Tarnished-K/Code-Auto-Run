from __future__ import annotations

from src.google_drive_client import GoogleDriveDocsClient


def main() -> int:
    client = GoogleDriveDocsClient.from_env(dry_run=False)
    client._build_services()
    print(f"Google OAuth token saved to {client.token_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
