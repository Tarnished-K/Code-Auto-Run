# TOOLING_LOG

## 2026-05-04

```json
{
  "date": "2026-05-04",
  "tool_name": "pytest",
  "tool_type": "python_package",
  "reason": "MVPの時間ガード、記事フォーマット、禁止表現、重複判定、ツールポリシーを自動検証するため",
  "source_url": "https://docs.pytest.org/",
  "permissions": ["local_read_only"],
  "risk_assessment": {
    "usefulness": 90,
    "safety": 90,
    "maintainability": 90,
    "officiality": 85,
    "testability": 95,
    "reversibility": 90
  },
  "decision": "added",
  "files_changed": ["requirements-dev.txt", "pyproject.toml", "tests/"],
  "tests_run": ["python -m pytest"],
  "rollback": "requirements-dev.txtからpytestを削除し、tests/を使わない運用に戻す"
}
```

```json
{
  "date": "2026-05-04",
  "tool_name": "google-api-python-client",
  "tool_type": "python_package",
  "reason": "Google Drive APIとGoogle Docs APIをPythonから直接呼び、記事在庫をGoogle Docsとして実保存するため",
  "source_url": "https://googleapis.github.io/google-api-python-client/",
  "permissions": [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/documents"
  ],
  "risk_assessment": {
    "usefulness": 95,
    "safety": 85,
    "maintainability": 85,
    "officiality": 90,
    "testability": 85,
    "reversibility": 85
  },
  "decision": "added",
  "files_changed": ["requirements-dev.txt", "pyproject.toml", "src/google_drive_client.py"],
  "tests_run": ["python -m pytest"],
  "rollback": "CODE_AUTO_RUN_DRY_RUN=trueに戻し、依存とGoogle APIクライアント実装を削除する"
}
```

```json
{
  "date": "2026-05-04",
  "tool_name": "tzdata",
  "tool_type": "python_package",
  "reason": "Windows環境でzoneinfoがAsia/Tokyoを解決できるようにし、稼働時間ガードを安定させるため",
  "source_url": "https://pypi.org/project/tzdata/",
  "permissions": ["local_read_only"],
  "risk_assessment": {
    "usefulness": 90,
    "safety": 90,
    "maintainability": 85,
    "officiality": 85,
    "testability": 95,
    "reversibility": 90
  },
  "decision": "added",
  "files_changed": ["requirements-dev.txt", "pyproject.toml"],
  "tests_run": ["python -m pytest"],
  "rollback": "requirements-dev.txtとpyproject.tomlからtzdataを削除する"
}
```
