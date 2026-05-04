# Code Auto Run

note向けの記事を Google Docs 形式で在庫化する自律生成システムのMVPです。

現フェーズでは note 投稿、note ログイン、非公式 API 利用は行いません。通常実行は JST 04:00〜07:00 に限定し、時間外は設計、テスト、ドキュメント更新だけを行います。

## MVP範囲

- 設定ファイル読み込み
- 稼働時間ガード
- 3ジャンル設定
- 記事フォーマット生成
- 禁止表現チェック
- リスク判定
- 重複フィンガープリント
- Google Docs 保存クライアントの dry-run / Google API 実保存
- 記事台帳
- GitHub Actions の朝実行 workflow

## ローカル実行

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest
python -m src.run_pipeline
```

`python -m src.run_pipeline` は時間外の場合、通常実行をスキップして `logs/runs/run.log` に記録します。

時間外にローカルで動作確認だけしたい場合は、外部書き込みをしないdry-runとして実行できます。

```powershell
python -m src.run_pipeline --test-run
```

## Google Docs実保存

デフォルトは安全のため `dry_run` です。実保存する場合は、Google Cloud ConsoleでOAuthクライアントを作成し、Drive APIとDocs APIを有効にしてください。

```powershell
New-Item -ItemType Directory -Force secrets
# OAuthクライアントJSONを secrets/google_oauth_client.json に配置
python -m src.setup_check
python -m src.google_auth_setup

$env:CODE_AUTO_RUN_DRY_RUN='false'
python -m src.run_pipeline
```

認証ファイルとトークンは `secrets/` 配下に置きます。このディレクトリは `.gitignore` 済みです。

## GPT-5.5で記事生成

デフォルトでは固定テンプレートを使います。GPT-5.5で本文生成する場合はOpenAI APIキーを環境変数に設定し、AI生成を有効化します。

```powershell
$env:OPENAI_API_KEY='sk-...'
$env:CODE_AUTO_RUN_USE_AI='true'
$env:OPENAI_MODEL='gpt-5.5'
python -m src.run_pipeline --test-run
```

または `.env.example` を参考に、Git管理外の `.env` に同じ値を保存できます。

`OPENAI_MODEL` はアカウントで利用できるモデルIDに合わせて変更できます。
