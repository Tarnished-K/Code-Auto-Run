# OPERATIONS

## 通常実行

通常実行は JST 04:00〜07:00 のみです。06:50以降は新規記事作成を開始しません。

## 時間外

時間外は通常実行をスキップします。許可される作業は設計、テスト、ドキュメント更新です。

ローカル検証だけ行う場合は、dry-run固定のテスト走行を使います。

```powershell
python -m src.run_pipeline --test-run
```

## Google Docs連携

デフォルトは `dry_run` です。ライブ書き込みを有効化する前に、Google OAuth、最小スコープ、承認済みDriveフォルダ、重複検出を確認してください。認証情報はGitに保存しません。

ライブ書き込みに必要な環境変数:

```text
CODE_AUTO_RUN_DRY_RUN=false
GOOGLE_OAUTH_CLIENT_PATH=secrets/google_oauth_client.json
GOOGLE_OAUTH_TOKEN_PATH=secrets/google_oauth_token.json
GOOGLE_DRIVE_ROOT_FOLDER=note記事ストック_自律生成
```

セットアップ確認:

```powershell
python -m src.setup_check
```

初回認証:

```powershell
python -m src.google_auth_setup
```

このコマンドはローカルブラウザでOAuth同意を行い、トークンを `secrets/google_oauth_token.json` に保存します。

## OpenAI記事生成

GPT-5.5で本文を生成する場合:

```powershell
$env:OPENAI_API_KEY='sk-...'
$env:CODE_AUTO_RUN_USE_AI='true'
$env:OPENAI_MODEL='gpt-5.5'
python -m src.run_pipeline --test-run
```

`CODE_AUTO_RUN_USE_AI` を設定しない場合は、固定テンプレートで記事本文を作ります。
