# AGENTS.md — note向け Google Docs 記事在庫 自律生成システム

最終更新: 2026-05-04 JST  
対象リポジトリ: `note-docs-stock-system`  
目的: Codex がこのドキュメントを読み、朝の指定時間だけ自律的に情報収集・記事作成・Google Drive/Google Docs への在庫保存を行う。

---

## 0. このドキュメントの使い方

このファイルは Codex に読み込ませるための永続指示ファイルである。リポジトリ直下に `AGENTS.md` として置くこと。

Codex は作業開始前にこのファイルを読み、以下を必ず守る。

- noteへの自動投稿は、現フェーズでは実装しない。
- 現フェーズの成果物は、Google Drive 上の3ジャンル別フォルダに格納される Google Docs 記事在庫である。
- 各記事は、noteで使えるように「無料部分」と「有料部分」を明確に区切る。
- YouTubeの再生数上位ノウハウ系動画を、需要調査・論点抽出・競合分析の参考にする。
- 人気動画の内容をそのまま要約して売らない。必ず独自の検証、テンプレート、手順、設定例、失敗ログ、チェックリストに変換する。
- 稼働時間は原則として JST 04:00〜07:00 のみ。
- 有用な Codex Skill、Plugin、MCP、外部ツール、ライブラリが見つかった場合、条件を満たせば自律的に追加してよい。
- ただし、認証情報、外部書き込み権限、個人情報、Cookie、非公式API、規約違反の可能性があるものは厳格に制御する。

---

## 1. システムの最終目的

このシステムは、note収益化のための記事を自動的に作る「記事在庫倉庫」である。

最終的な流れは以下。

```text
朝4時〜7時の稼働ウィンドウで起動
↓
対象ジャンルを選ぶ
↓
YouTube再生数上位のノウハウ系動画を調査
↓
公式情報・一次情報・信頼できる情報でファクトチェック
↓
読者ニーズ、競合の不足点、売れる切り口を抽出
↓
note向け記事を作成
↓
無料部分 / 有料部分を分ける
↓
有料部分にテンプレート・手順・失敗例・検証ログを入れる
↓
リスクチェック・禁止表現チェック・重複チェック
↓
Google Docs形式で作成
↓
Google Drive上の対応ジャンルフォルダへ保存
↓
記事台帳・実行ログに記録
↓
07:00前に安全停止
```

このシステムは投稿ボタンを押すためのシステムではない。  
noteへの投稿、販売設定、有料ライン設定、BrowserMCPによる投稿自動化は、後で別システムとして作る。

---

## 2. 現フェーズのスコープ

### 2.1 やること

- note向け記事テーマの発見
- ニッチかつ需要がありそうな3ジャンルの運用
- YouTube上位動画を使った需要調査
- 公式情報・一次情報によるファクトチェック
- 無料部分 / 有料部分に分かれた記事の作成
- Google Docs形式での記事保存
- Google Driveのジャンル別フォルダへの格納
- 記事台帳の作成・更新
- 生成記事の品質チェック
- 朝4時〜7時だけの自律稼働
- 有用なツール・MCP・Codex Skillの自律追加

### 2.2 やらないこと

- noteへの自動投稿
- noteへの自動ログイン
- noteの非公式API利用
- note内部APIの解析
- Cookie、CSRFトークン、セッション情報の抽出
- CAPTCHA回避
- 他人のYouTube動画の全文転載
- 字幕や台本を丸ごと保存して販売用にリライトすること
- 「必ず稼げる」などの誇大表現
- 法律、税金、投資、医療に関する断定的助言
- スパム的な大量記事生成

---

## 3. noteに関する前提

### 3.1 note公式APIについて

noteは公式に公開された投稿APIを提供していない。  
したがって、現フェーズではnote投稿を自動化しない。

禁止:

```text
- note非公式APIを使う
- ブラウザ開発者ツールで内部APIを解析して投稿する
- Cookieを抜き出して保存する
- CSRFトークンをプログラムから利用する
- noteのログイン情報を .env に保存する
- noteの投稿ボタンを自動クリックする
```

許可:

```text
- noteで投稿するための記事をGoogle Docsに在庫化する
- noteの有料ライン候補をGoogle Docs内に明記する
- 手動投稿時に使いやすい形式へ整形する
- 将来の投稿システムに渡せるメタデータを保存する
```

### 3.2 有料ラインの設計

noteの有料ラインは段落間に設定する。  
したがってGoogle Docs内でも、有料ライン候補を独立段落で明記する。

必須マーカー:

```text
【無料部分ここから】

...

【NOTE有料ライン候補：この段落の直後に有料ラインを設定】

【有料部分ここから】
```

このマーカーは記事本文内で必ず独立した段落として置く。

---

## 4. 3ジャンルの運用方針

現時点では、以下の3ジャンルを扱う。  
Google Drive上にも同名フォルダを作成する。

### 4.1 ジャンル1: AIエージェント・自動化・実験ログ

フォルダ名:

```text
01_AIエージェント_自動化_実験ログ
```

扱うテーマ:

- Codex活用
- MCP活用
- BrowserMCP活用
- AIエージェント設計
- 自動化ワークフロー
- Google Docs/Drive自動化
- n8n、Make、Zapier等の業務自動化
- AIで記事制作を半自動化する実験
- 実際に作った仕組みの検証ログ

有料部分に入れるべき価値:

- 実際に動いた設定ファイル
- AGENTS.mdテンプレート
- プロンプト
- MCP設定例
- 失敗ログ
- 改善前後
- チェックリスト
- 実装手順

避ける表現:

- 「完全放置で稼げる」
- 「誰でも必ず収益化」
- 「自動で月○万円確定」

望ましいタイトル例:

```text
Codexでnote記事在庫を自動生成する仕組みを作った実験ログ
AIエージェントにGoogle Docs記事倉庫を作らせる手順と失敗例
BrowserMCPを投稿ではなく需要調査に使う安全な設計
```

---

### 4.2 ジャンル2: 個人事業・中小企業向け Google Workspace 効率化

フォルダ名:

```text
02_個人事業_中小企業_GoogleWorkspace効率化
```

扱うテーマ:

- Google Drive整理
- Google Docsテンプレート
- Google Sheets管理表
- Gmail業務効率化
- 個人事業主の業務導線
- 小規模チームのAI活用
- 請求、案件、発信、問い合わせ管理
- Google Workspace + AIエージェントの実務活用

有料部分に入れるべき価値:

- フォルダ設計テンプレート
- Google Docs記事管理テンプレート
- Google Sheets台帳テンプレート
- Apps Scriptサンプル
- 業務フロー図
- 導入チェックリスト
- 小規模運用の失敗例

望ましいタイトル例:

```text
個人事業主がGoogle DriveをAI前提で整理するフォルダ設計
Google Docsで記事在庫を管理するための実務テンプレート
小規模事業者向け：Google WorkspaceをAIエージェントが扱いやすくする設計
```

---

### 4.3 ジャンル3: YouTubeリサーチ・発信コンテンツ設計

フォルダ名:

```text
03_YouTubeリサーチ_発信コンテンツ設計
```

扱うテーマ:

- YouTube上位動画から需要を読む方法
- ノウハウ系動画のタイトル分析
- 視聴者コメントから悩みを抽出
- note記事化の切り口設計
- 人気動画の不足点を補う有料記事設計
- 発信テーマの選定
- X、note、ブログ、YouTube台本への展開

有料部分に入れるべき価値:

- YouTube調査テンプレート
- キーワードリサーチ表
- タイトル分析表
- 競合不足点チェックリスト
- note記事化プロンプト
- 無料部分 / 有料部分の構成テンプレート
- 具体的なリサーチログ

禁止:

```text
- 人気動画の要約だけを売る
- 動画台本をリライトして売る
- 字幕全文を保存して記事化する
- 著作権者の表現を実質的に複製する
```

望ましいタイトル例:

```text
YouTube上位動画からnote有料記事の需要を見つけるリサーチ手順
人気ノウハウ動画10本を「要約」ではなく「商品設計」に変換する方法
YouTube再生数から読者の悩みを読むためのチェックリスト
```

---

## 5. Google Drive / Google Docs 保存設計

### 5.1 Google Driveフォルダ構成

Google Drive上に以下のルートフォルダを作る。

```text
note記事ストック_自律生成
```

その下に3フォルダを作る。

```text
note記事ストック_自律生成/
  01_AIエージェント_自動化_実験ログ/
  02_個人事業_中小企業_GoogleWorkspace効率化/
  03_YouTubeリサーチ_発信コンテンツ設計/
```

補助的に、ローカルまたはDrive内に以下の管理ファイルを作ってよい。

```text
記事台帳
実行ログ
リサーチログ
ツール追加ログ
```

ただし、ユーザーが「フォルダは3つだけにしたい」と明示した場合は、Drive上に追加フォルダを作らず、台帳はローカルJSONまたは1つのGoogle Sheetsにする。

### 5.2 Google Docs記事タイトル命名規則

Google Docsのタイトルは以下の形式にする。

```text
YYYY-MM-DD__ジャンル番号__記事タイトル__status
```

例:

```text
2026-05-04__01__CodexでGoogleDocs記事在庫を作る実験ログ__stock_draft
```

ステータス:

```text
stock_draft      記事在庫として保存済み
needs_review     人間確認が必要
source_missing   出典不足
risk_hold        規約・法務・誤情報リスクあり
duplicate_hold   類似記事が既に存在
```

### 5.3 Google Docs本文フォーマット

各記事は1つのGoogle Docsにまとめる。  
本文構成は必ず以下に従う。

```text
# 記事タイトル

【管理メタデータ】
ジャンル:
ステータス:
作成日:
想定読者:
想定価格:
想定販売形式:
リスクレベル:
品質スコア:
主要ソース:
YouTube参照動画:
記事フィンガープリント:

---

【記事の狙い】
この記事が解決する悩み:
読者が有料部分で得るもの:
競合との差分:
独自価値:

---

【無料部分ここから】

## 導入

## 結論

## なぜ今このテーマが重要か

## 全体像

## 有料部分で扱う内容の予告

【NOTE有料ライン候補：この段落の直後に有料ラインを設定】

【有料部分ここから】

## 具体手順

## 実験ログ / 検証ログ

## テンプレート

## プロンプト

## 設定ファイル例

## 失敗例と対処法

## チェックリスト

## 応用例

## まとめ

---

【参考ソース】
- Source 1:
- Source 2:
- Source 3:

---

【投稿前チェック】
- [ ] 盗作・剽窃ではない
- [ ] YouTube動画の要約だけになっていない
- [ ] 誇大表現がない
- [ ] 「必ず儲かる」系表現がない
- [ ] 事実情報に出典がある
- [ ] 無料部分だけでも読者に価値がある
- [ ] 有料部分に具体物がある
- [ ] noteの有料ライン候補が独立段落になっている
```

### 5.4 無料部分と有料部分の目安

無料部分:

```text
- 読者の悩みを明確にする
- 結論を一部出す
- 全体像を説明する
- 信頼を作る
- 有料部分で得られる具体物を予告する
```

有料部分:

```text
- 実装手順
- テンプレート
- プロンプト
- 設定ファイル
- 検証ログ
- 失敗例
- 改善例
- チェックリスト
- そのまま使える成果物
```

悪い有料部分:

```text
- 抽象論だけ
- 人気動画の要約だけ
- 無料部分と内容が重複
- 「がんばりましょう」で終わる
- 出典なしの断定
```

---

## 6. YouTubeリサーチ方針

### 6.1 YouTubeの役割

YouTubeは以下の目的で使う。

```text
需要調査
競合分析
タイトル傾向の把握
視聴者の悩み抽出
無料で出回っている情報の範囲把握
有料記事で補える不足点の発見
```

YouTubeは事実確認の最終ソースではない。  
事実確認は公式ドキュメント、一次情報、信頼できる情報源で行う。

### 6.2 取得する情報

YouTube Data API等で、可能な範囲で以下を取得する。

```text
video_id
title
channel_title
published_at
view_count
like_count
comment_count
duration
description
tags
top_comments_if_allowed
url
```

優先する動画:

```text
- ノウハウ系
- 実務系
- 解説系
- 視聴回数が多い
- コメントが多い
- 直近1〜24ヶ月以内
- 日本語または日本市場に関係する
- 視聴者の悩みがコメントに出ている
```

除外する動画:

```text
- Shorts中心
- 明らかな煽り商材
- 根拠のない収益保証
- 違法性が疑われる内容
- 医療・投資・法律の断定助言
- 個人攻撃・炎上煽り
- 著作権侵害コンテンツ
- 古すぎて仕様が変わっている可能性が高い動画
```

### 6.3 再生数上位動画の使い方

再生数が多い動画は「需要がある可能性」を示す。  
しかし、再生数が多いことは「正しいこと」を意味しない。

Codex は必ず以下を分ける。

```text
YouTube動画:
  需要、悩み、タイトル、競合構成を見る

公式情報:
  正確な仕様、料金、API、利用条件を見る

自分の検証:
  有料部分の価値にする
```

### 6.4 動画内容理解の前提

GPTは、動画のフレーム、字幕、文字起こし、説明欄、コメントなどを組み合わせて動画内容を把握できる。  
ただし、このシステムは「URLを渡せば常に動画全体を完全理解できる」前提で設計しない。

現実的な安定運用:

```text
1. YouTube Data APIでメタデータと統計情報を取得
2. 説明欄とタイトルからテーマを抽出
3. 利用可能かつ権利上問題ない字幕・文字起こしだけを参照
4. 必要な場合のみ、動画の一部フレームや視聴メモで補完
5. 複数動画の共通論点を抽出
6. 公式情報でファクトチェック
7. 自分の検証・テンプレート・実験ログに変換
```

### 6.5 字幕・文字起こしの扱い

禁止:

```text
- 非公式APIで字幕を抜く
- 隠しエンドポイントを叩く
- 字幕全文を保存する
- 動画台本をリライトして販売する
- 動画1本の要約だけを有料記事にする
```

許可:

```text
- 公開情報として利用可能な範囲の要点把握
- 公式APIや利用条件に沿った取得
- 自分用の短い分析メモ
- 複数動画から共通ニーズを抽出
- 出典として動画URL・タイトル・チャンネル名を記録
```

### 6.6 YouTube由来記事の価値変換ルール

悪い変換:

```text
人気動画10本を要約しました
```

良い変換:

```text
人気動画で語られていた需要をもとに、
実際にCodex + Google Docsで記事在庫システムを作り、
動いた設定、失敗ログ、テンプレート、チェックリストに落とし込んだ
```

---

## 7. 情報収集・記事生成パイプライン

### 7.1 毎回の実行フロー

```text
1. runtime_window_guard を通過する
2. 実行ロックを取得する
3. 記事台帳を読み込む
4. 直近の生成履歴を確認する
5. 対象ジャンルを選ぶ
6. キーワード候補を作る
7. YouTube再生数上位動画を調査する
8. 競合構成・視聴者ニーズ・不足点を抽出する
9. 公式情報・一次情報を集める
10. 記事企画をスコアリングする
11. 品質基準を満たす企画だけ記事化する
12. 無料部分 / 有料部分に分けて草稿を作る
13. ファクトチェックする
14. 禁止表現チェックする
15. 重複チェックする
16. 品質スコアを付ける
17. Google Docsとして保存する
18. 対応ジャンルフォルダへ格納する
19. 記事台帳に記録する
20. 実行ログを保存する
21. ロックを解放して終了する
```

### 7.2 企画スコアリング

各企画を100点満点で評価する。

```yaml
scoring:
  reader_pain:
    weight: 20
    description: "読者の悩みが明確か"
  paid_value:
    weight: 20
    description: "有料部分に具体物を入れられるか"
  originality:
    weight: 20
    description: "自分の検証・設定・失敗ログを入れられるか"
  freshness:
    weight: 10
    description: "今読む理由があるか"
  youtube_demand:
    weight: 10
    description: "YouTube上位動画やコメントから需要が見えるか"
  source_reliability:
    weight: 10
    description: "公式情報・一次情報で裏取りできるか"
  risk_safety:
    weight: 10
    description: "規約・法務・誤情報リスクが低いか"
```

記事化条件:

```text
score >= 80:
  stock_draft としてGoogle Docsへ保存

65 <= score < 80:
  needs_review として保存するか、改善して再評価

score < 65:
  記事化しない。リサーチログだけ残す。
```

### 7.3 記事の必須品質

記事は以下を満たすこと。

```text
- 読者の悩みが冒頭で明確
- 無料部分だけでも価値がある
- 有料部分に具体物がある
- YouTube要約だけではない
- 公式情報で事実確認されている
- 出典が本文末尾にある
- 誇大表現がない
- 有料ライン候補が明確
- 3ジャンルのどれかに分類されている
- Google Docsとして保存できる
```

---

## 8. リスク管理・禁止表現

### 8.1 高リスク領域

以下は自動生成・自動ストック時に注意する。

```text
法律
税金
投資
医療
薬機法に関わる健康情報
就職・転職の断定助言
金融商品
仮想通貨
政治的主張
センシティブな個人情報
他者批判
収益保証
```

高リスク領域の記事は、`risk_hold` または `needs_review` にする。  
自動で `stock_draft` 扱いにしない。

### 8.2 禁止表現

以下のような表現は禁止。

```text
必ず稼げる
誰でも稼げる
放置で稼げる
完全自動で収益確定
月収保証
再現性100%
ノーリスク
初心者でも絶対成功
たった○日で必ず○万円
裏技で確実に稼ぐ
人生が確実に変わる
この方法だけで十分
公式より正しい
```

### 8.3 推奨表現

安全で信頼されやすい表現に変換する。

```text
検証してわかった
自分の環境ではこう動いた
実験ログとして共有する
再現時に確認すべきポイント
失敗した部分も含めて整理する
収益保証ではなく仕組み化の記録
実務テンプレートとして使えるようにした
```

### 8.4 YouTube関連の権利リスク

禁止:

```text
- 動画の台本をほぼ同じ構成で記事化する
- 字幕を全文保存して使う
- サムネイル画像を無断転載する
- 動画内の図表をそのまま転載する
- 「この動画の有料要約」として販売する
```

許可:

```text
- 動画から需要や論点を学ぶ
- 複数動画の共通傾向を分析する
- 自分で検証した結果を記事化する
- 動画URLを参考ソースとして記録する
- 自分の図表・テンプレートを作る
```

---

## 9. 稼働時間ポリシー

### 9.1 許可された稼働時間

このシステムは以下の時間帯だけ稼働する。

```yaml
runtime_window:
  timezone: "Asia/Tokyo"
  start: "04:00"
  end: "07:00"
  hard_stop_new_tasks: "06:50"
  max_articles_per_run: 1
  allow_manual_run_outside_window: false
  require_lock: true
  duplicate_policy: "skip_if_same_title_or_source"
```

### 9.2 ルール

Codex は以下を必ず守る。

```text
- JST 04:00〜07:00 以外に通常実行しない
- 起動時に現在時刻を確認する
- 新しい記事生成を始める前に現在時刻を確認する
- 06:50以降は新しい記事生成を開始しない
- 07:00に到達したら、現在のatomic stepを終え、状態保存して停止する
- 1回の実行で最大1記事を基本とする
- 実行ごとにログを保存する
- 同時実行を防ぐためロックを使う
- 同じ記事を重複作成しない
```

### 9.3 推奨スケジューラー

最初はGitHub Actionsを推奨する。

`.github/workflows/morning-run.yml` の例:

```yaml
name: note-docs-stock-morning-run

on:
  schedule:
    - cron: "*/30 4-6 * * *"
      timezone: "Asia/Tokyo"
  workflow_dispatch:

concurrency:
  group: note-docs-stock-pipeline
  cancel-in-progress: false

jobs:
  run:
    runs-on: ubuntu-latest
    timeout-minutes: 25

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run morning stock pipeline
        run: |
          python -m src.run_pipeline \
            --timezone Asia/Tokyo \
            --window-start 04:00 \
            --window-end 07:00 \
            --hard-stop 06:50 \
            --max-articles 1
```

### 9.4 Python時間ガード例

```python
from datetime import datetime, time
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("Asia/Tokyo")
WINDOW_START = time(4, 0)
WINDOW_END = time(7, 0)
HARD_STOP = time(6, 50)

def now_jst() -> datetime:
    return datetime.now(TIMEZONE)

def is_within_runtime_window(now: datetime | None = None) -> bool:
    now = now or now_jst()
    return WINDOW_START <= now.time() < WINDOW_END

def can_start_new_article(now: datetime | None = None) -> bool:
    now = now or now_jst()
    return WINDOW_START <= now.time() < HARD_STOP

def assert_runtime_window() -> None:
    if not is_within_runtime_window():
        raise RuntimeError("Runtime window closed: allowed only between 04:00 and 07:00 JST.")
```

---

## 10. 自律ツール追加ポリシー

### 10.1 基本方針

Codex は、この自律システムの品質・安定性・安全性・収益性を高めるために、有用な追加ツール、Codex Skill、Plugin、MCP、Python/npmライブラリ、Google Workspace連携を見つけた場合、条件を満たせば自律的に追加してよい。

この許可は以下に限定される。

```text
- Google Docs記事在庫化を改善するもの
- YouTubeリサーチを改善するもの
- ファクトチェックを改善するもの
- 記事品質チェックを改善するもの
- リスクチェックを改善するもの
- 実行時間制御、ロック、重複防止を改善するもの
- Google Drive/Docs保存を安定化するもの
- Codexの作業効率を高めるSkill/Plugin/MCP
```

### 10.2 自律追加してよいもの

以下は、条件を満たせばCodexが自律追加してよい。

```text
Codex Skill:
  - youtube-research-skill
  - google-docs-stock-writer-skill
  - note-article-format-skill
  - risk-checker-skill
  - fact-checker-skill
  - tool-discovery-skill
  - runtime-window-skill

MCP:
  - Google Workspace MCP
  - Google Drive MCP
  - Google Docs / Drive操作に使える信頼済みMCP
  - BrowserMCP
  - GitHub MCP
  - 検索系MCP
  - ファイル管理系MCP

ライブラリ:
  - google-api-python-client
  - google-auth
  - google-auth-oauthlib
  - pydantic
  - PyYAML
  - python-dotenv
  - tenacity
  - pytest
  - ruff
  - mypy
  - typer
  - rich
  - dateparser
  - isodate
  - tiktoken またはトークン計測用ライブラリ
```

ただし、追加前に必ず以下を確認する。

```text
- 公式ドキュメントまたは信頼できるリポジトリがある
- ライセンスが利用可能
- 最近メンテナンスされている
- 目的に合っている
- 過剰な権限を要求しない
- 認証情報を外部へ送らない
- テスト可能である
- アンインストールまたは無効化が可能
```

### 10.3 追加してはいけないもの

以下は追加禁止。

```text
- note非公式API投稿ツール
- note内部API解析ツール
- Cookie抽出ツール
- CAPTCHA回避ツール
- セッションハイジャック系ツール
- YouTube字幕を非公式に大量取得するツール
- 著作権侵害コンテンツ取得ツール
- 認証情報を外部サーバーへ送るツール
- 出所不明のMCP
- インストール時に不明なpostinstall処理を行うnpmパッケージ
- 任意コード実行リスクが高い未検証ツール
- 金融、投資、医療、法律助言を自動生成する専用ツール
- スパム投稿、量産投稿、SNS自動拡散ツール
```

### 10.4 追加時の判断基準

Codexは以下のスコアを付ける。

```yaml
tool_evaluation:
  usefulness:
    weight: 25
    description: "このシステムの成果物品質を上げるか"
  safety:
    weight: 25
    description: "権限・認証情報・外部送信リスクが低いか"
  maintainability:
    weight: 15
    description: "メンテナンスされているか"
  officiality:
    weight: 15
    description: "公式または広く信頼されているか"
  testability:
    weight: 10
    description: "自動テストできるか"
  reversibility:
    weight: 10
    description: "無効化・削除しやすいか"
```

判定:

```text
score >= 85:
  自律追加してよい

70 <= score < 85:
  追加してよいが、TOOLING_LOG.mdに理由を詳しく残す

score < 70:
  追加しない。候補として記録するだけ。
```

### 10.5 権限レベル別の扱い

```yaml
permission_policy:
  local_read_only:
    auto_add: true
    examples:
      - lint tool
      - formatter
      - local parser
      - article quality checker

  local_write_project:
    auto_add: true
    requirements:
      - update TOOLING_LOG.md
      - update requirements.txt or package.json
      - add tests
      - run tests

  external_read_only:
    auto_add: true
    requirements:
      - use official API where possible
      - use least privilege OAuth scopes
      - document scopes
      - never store secrets in repo

  external_write_google_drive_docs:
    auto_add: true
    requirements:
      - write only to approved Drive folders
      - use least privilege scopes
      - log created document IDs
      - implement dry_run mode
      - implement duplicate detection

  browser_control:
    auto_add: conditional
    requirements:
      - only for research or future supervised workflows
      - no note posting in current phase
      - no CAPTCHA bypass
      - no credential extraction
      - no hidden endpoint usage

  credential_expansion:
    auto_add: false
    action:
      - create setup instructions
      - do not request or store secrets
      - use environment variables or secret manager
```

### 10.6 ツール追加時の必須ログ

Codexがツールを追加した場合、必ず `docs/TOOLING_LOG.md` または `logs/tooling/YYYY-MM-DD.json` に記録する。

記録項目:

```json
{
  "date": "2026-05-04",
  "tool_name": "example-tool",
  "tool_type": "mcp|skill|plugin|python_package|npm_package",
  "reason": "why this was useful",
  "source_url": "official docs or repo",
  "permissions": ["drive.file"],
  "risk_assessment": {
    "usefulness": 90,
    "safety": 85,
    "maintainability": 80,
    "officiality": 90,
    "testability": 75,
    "reversibility": 80
  },
  "decision": "added|rejected|candidate",
  "files_changed": [],
  "tests_run": [],
  "rollback": "how to disable or remove"
}
```

### 10.7 推奨MCP/ツール候補

#### Google Workspace MCP

目的:

```text
Google Drive/Docs/Gmail/Calendar等との接続。
現フェーズでは主にDrive/Docsの検索・読み取り・作成補助に使う。
```

注意:

```text
- Developer Preview等の位置づけなら安定性を過信しない
- OAuthスコープは最小限にする
- 読み取り・書き込み対象を記事在庫フォルダに限定する
- AIが外部入力に触れる場合、間接プロンプトインジェクションに注意する
```

#### BrowserMCP

目的:

```text
ブラウザ上でしか確認できない情報の調査、将来の投稿システム検証、画面確認。
```

現フェーズでの制限:

```text
- note投稿には使わない
- noteログインには使わない
- Cookieやパスワードを扱わない
- CAPTCHA回避しない
- 研究用・確認用に限定する
```

#### Codex Skills

作るべきSkill:

```text
skills/
  youtube-research/
    SKILL.md
  article-stock-writer/
    SKILL.md
  risk-checker/
    SKILL.md
  google-docs-exporter/
    SKILL.md
  runtime-window/
    SKILL.md
  tool-discovery/
    SKILL.md
```

Skillは反復ワークフローを安定させるために作る。  
単発作業ではなく、何度も使う作業をSkill化する。

#### Subagents

複雑な実行では、Codexは以下のサブエージェントを使ってよい。

```text
ResearchAgent:
  YouTubeとWeb情報の調査

FactCheckAgent:
  公式情報・一次情報で裏取り

WriterAgent:
  note記事本文の作成

RiskAgent:
  規約・誇大表現・権利リスク確認

DocsPublisherAgent:
  Google Docs作成とDrive格納

ToolingAgent:
  MCP/Skill/Plugin/ライブラリの評価と追加
```

---

## 11. リポジトリ構成

推奨構成:

```text
note-docs-stock-system/
  AGENTS.md
  README.md
  PLANS.md

  .codex/
    config.toml

  .github/
    workflows/
      morning-run.yml

  config/
    runtime_window.yaml
    genres.yaml
    youtube_research.yaml
    risk_policy.yaml
    banned_claims.yaml
    google_drive.yaml
    tool_policy.yaml
    article_quality.yaml

  skills/
    youtube-research/
      SKILL.md
    article-stock-writer/
      SKILL.md
    risk-checker/
      SKILL.md
    google-docs-exporter/
      SKILL.md
    runtime-window/
      SKILL.md
    tool-discovery/
      SKILL.md

  prompts/
    researcher.md
    article_writer.md
    fact_checker.md
    risk_checker.md
    google_docs_writer.md
    tool_discovery.md

  src/
    __init__.py
    run_pipeline.py
    runtime_window_guard.py
    lock_manager.py
    config_loader.py
    youtube_research_agent.py
    source_collector.py
    fact_checker.py
    article_planner.py
    article_writer.py
    article_format.py
    risk_checker.py
    banned_claims.py
    duplicate_checker.py
    google_drive_client.py
    google_docs_writer.py
    ledger.py
    tool_discovery_agent.py

  apps_script/
    stock_writer.gs

  data/
    research_cache/
    source_snapshots/
    article_fingerprints/
    sales_csv/

  outputs/
    local_drafts/
    pending_drive/
    rejected/

  logs/
    runs/
    tooling/
    errors/

  docs/
    TOOLING_LOG.md
    SOURCE_POLICY.md
    OPERATIONS.md

  tests/
    test_runtime_window_guard.py
    test_article_format.py
    test_banned_claims.py
    test_risk_checker.py
    test_duplicate_checker.py
```

---

## 12. 設定ファイル例

### 12.1 `config/genres.yaml`

```yaml
genres:
  - id: "01"
    key: "ai_agents_automation_logs"
    folder_name: "01_AIエージェント_自動化_実験ログ"
    description: "Codex、MCP、AIエージェント、自動化、実験ログ"
    priority: 1
    default_price_range_jpy: [980, 2980]

  - id: "02"
    key: "google_workspace_efficiency"
    folder_name: "02_個人事業_中小企業_GoogleWorkspace効率化"
    description: "Google Workspace、個人事業、中小企業の業務効率化"
    priority: 2
    default_price_range_jpy: [500, 1980]

  - id: "03"
    key: "youtube_research_content_design"
    folder_name: "03_YouTubeリサーチ_発信コンテンツ設計"
    description: "YouTube需要調査、発信設計、note記事化"
    priority: 3
    default_price_range_jpy: [980, 2480]
```

### 12.2 `config/youtube_research.yaml`

```yaml
youtube_research:
  enabled: true
  api_provider: "youtube_data_api"
  region_code: "JP"
  relevance_language: "ja"
  order: "viewCount"
  max_results_per_query: 10
  max_videos_per_article: 8
  exclude_shorts: true
  min_duration_seconds: 240
  max_duration_seconds: 7200
  published_after_months: 24
  use_comments: true
  max_comments_per_video: 20
  transcript_policy:
    use_transcripts: "only_when_legally_and_technically_allowed"
    store_full_transcript: false
    store_short_notes_only: true
    max_quote_chars_per_video: 120
  banned_video_signals:
    - "必ず稼げる"
    - "誰でも月収"
    - "放置で"
    - "絶対成功"
    - "裏技"
```

### 12.3 `config/risk_policy.yaml`

```yaml
risk_levels:
  low:
    auto_stock_allowed: true
    examples:
      - "自分の作業ログ"
      - "プロンプト集"
      - "Google Docsテンプレート"
      - "AIエージェント実験ログ"

  medium:
    auto_stock_allowed: true
    requires_extra_check: true
    examples:
      - "副業ノウハウ"
      - "業務効率化"
      - "YouTube発信設計"

  high:
    auto_stock_allowed: false
    status: "needs_review"
    examples:
      - "法律"
      - "税金"
      - "投資"
      - "医療"
      - "薬機法"
      - "規約解釈の断定"
```

### 12.4 `config/banned_claims.yaml`

```yaml
banned_claims:
  - "必ず稼げる"
  - "誰でも稼げる"
  - "放置で稼げる"
  - "完全自動で収益確定"
  - "月収保証"
  - "再現性100%"
  - "ノーリスク"
  - "絶対成功"
  - "確実に儲かる"
  - "最短で確実に"
  - "裏技で稼ぐ"
```

### 12.5 `config/tool_policy.yaml`

```yaml
tool_auto_add:
  enabled: true
  default_decision: "evaluate_then_add_if_safe"
  minimum_score_for_auto_add: 85
  minimum_score_for_candidate: 70

  allowed_categories:
    - "codex_skill"
    - "codex_plugin"
    - "mcp_server"
    - "python_package"
    - "npm_package"
    - "github_action"
    - "google_api_client"

  trusted_sources:
    - "OpenAI official docs"
    - "Google official docs"
    - "GitHub official docs"
    - "BrowserMCP official docs"
    - "well maintained open source repositories"

  disallowed_categories:
    - "unofficial_note_api"
    - "cookie_extractor"
    - "captcha_bypass"
    - "session_hijacking"
    - "youtube_transcript_scraper_unofficial"
    - "spam_automation_tool"

  require_log: true
  require_tests: true
  require_rollback_instructions: true
```

---

## 13. Google Drive / Docs 実装方針

### 13.1 MVP優先順位

最初は以下の順で実装する。

```text
1. ローカルMarkdown記事生成
2. Google Driveフォルダ作成
3. Google Docs作成
4. 対応フォルダへの移動
5. 記事台帳更新
6. YouTube調査の自動化
7. 品質チェックの強化
8. Tool/MCP自律追加
```

### 13.2 Google Drive API

Driveフォルダは `application/vnd.google-apps.folder` として作成する。  
Google Docsは `application/vnd.google-apps.document` として扱う。

### 13.3 Google Docs API

本文挿入や更新には `documents.batchUpdate` を使う。  
Apps Scriptを使う場合は `DriveApp` と `DocumentApp` を使ってもよい。

### 13.4 OAuthと認証情報

禁止:

```text
- credentials.json をGit管理する
- token.json をGit管理する
- APIキーをログに出す
- OAuthトークンを記事本文や台帳に保存する
```

許可:

```text
- GitHub Actions Secrets
- Google Cloud Secret Manager
- ローカル .env
- .gitignoreされた認証ファイル
```

必須:

```text
- .gitignoreに認証情報を追加
- 最小権限スコープを使う
- Drive書き込み対象を記事在庫フォルダに限定する
```

---

## 14. 重複防止・台帳管理

### 14.1 記事フィンガープリント

記事ごとに以下からフィンガープリントを作る。

```text
genre_key
normalized_title
youtube_video_ids
main_keywords
source_urls
```

同じフィンガープリントが存在する場合、新規作成しない。

### 14.2 台帳項目

記事台帳には以下を保存する。

```json
{
  "article_id": "2026-05-04-ai-agents-001",
  "title": "CodexでGoogle Docs記事在庫を作る実験ログ",
  "genre_key": "ai_agents_automation_logs",
  "status": "stock_draft",
  "created_at": "2026-05-04T04:30:00+09:00",
  "drive_folder_id": "xxx",
  "google_doc_id": "xxx",
  "google_doc_url": "xxx",
  "fingerprint": "xxx",
  "quality_score": 86,
  "risk_level": "low",
  "source_urls": [],
  "youtube_video_ids": [],
  "estimated_price_jpy": 1480
}
```

---

## 15. Codexへの作業指示

Codexはこのシステムを改善・実行するとき、以下の順で動く。

```text
1. AGENTS.mdを読む
2. 現在時刻がJST 04:00〜07:00か確認
3. 時間外なら通常実行はせず、設計・テスト・ドキュメント更新のみ行う
4. 実行ロックを確認
5. 設定ファイルを読む
6. 欠けている実装を補う
7. 必要なら有用なツール・MCP・Skillを評価して追加する
8. テストを追加・実行する
9. 1記事だけ生成する
10. Google Docsへ保存する
11. 台帳とログを更新する
12. 07:00前に停止する
```

### 15.1 初回Codexプロンプト

Codexに最初に渡すプロンプト例:

```text
このリポジトリのAGENTS.mdを読んでください。
目的は、note向けの記事をGoogle Docs形式で在庫化する自律システムを作ることです。

現フェーズではnote投稿は行いません。
Google Drive上に3ジャンルのフォルダを作り、各ジャンルに対応したGoogle Docs記事を保存します。
記事は無料部分と有料部分を明確に区切ってください。
YouTubeの再生数上位ノウハウ系動画を需要調査に使い、公式情報でファクトチェックしてください。
朝4時〜7時JSTだけ稼働する時間ガードを実装してください。
有用なCodex Skill、Plugin、MCP、ライブラリが見つかった場合は、AGENTS.mdのツール追加ポリシーに従って自律追加してよいです。

まずはMVPとして以下を実装してください。
- config読み込み
- runtime_window_guard
- 3ジャンル設定
- 記事フォーマッタ
- 禁止表現チェッカー
- 重複チェッカー
- Google Docs保存クライアントの雛形
- 記事台帳
- GitHub Actionsの朝実行workflow
- テスト

完了条件:
- pytestが通る
- 時間外実行時は安全に終了する
- サンプル記事をGoogle Docs保存用フォーマットに変換できる
- 3ジャンルのどれかに分類できる
- 無料部分 / 有料部分 / 有料ライン候補マーカーが必ず入る
- TOOLING_LOG.mdが存在する
```

---

## 16. 品質チェックリスト

記事をGoogle Docsへ保存する前に、以下を検査する。

```text
構成:
- [ ] タイトルがある
- [ ] 管理メタデータがある
- [ ] 無料部分マーカーがある
- [ ] 有料ライン候補マーカーがある
- [ ] 有料部分マーカーがある
- [ ] 参考ソース欄がある

内容:
- [ ] 読者の悩みが明確
- [ ] 無料部分に価値がある
- [ ] 有料部分に具体物がある
- [ ] YouTube要約だけではない
- [ ] 独自検証またはテンプレートがある
- [ ] 失敗例または注意点がある

安全:
- [ ] 禁止表現がない
- [ ] 収益保証がない
- [ ] 高リスク領域ならneeds_review
- [ ] 著作権侵害リスクが低い
- [ ] 出典が記録されている
- [ ] 個人情報が含まれていない

運用:
- [ ] ジャンル分類済み
- [ ] フィンガープリント生成済み
- [ ] 重複していない
- [ ] Google Docs保存先フォルダが正しい
- [ ] 台帳に記録された
```

---

## 17. テスト方針

必須テスト:

```text
test_runtime_window_guard.py:
  - 03:59 JST は実行不可
  - 04:00 JST は実行可
  - 06:49 JST は新規記事開始可
  - 06:50 JST は新規記事開始不可
  - 07:00 JST は実行不可

test_article_format.py:
  - 無料部分マーカーが入る
  - 有料ライン候補マーカーが独立段落
  - 有料部分マーカーが入る
  - 管理メタデータが入る

test_banned_claims.py:
  - 禁止表現を検出する
  - 許容表現は誤検出しすぎない

test_duplicate_checker.py:
  - 同じ動画IDとタイトルなら重複判定
  - 別ジャンルなら必要に応じて別記事扱い

test_tool_policy.py:
  - 禁止ツールを拒否する
  - 安全なローカルツールは候補化する
  - 外部書き込みツールは権限チェックを要求する
```

---

## 18. 運用ループ

### 18.1 毎朝

```text
04:00〜07:00:
  - 自動起動
  - 最大1記事生成
  - Google Docs保存
  - 台帳更新
  - ログ保存
```

### 18.2 週次

```text
- 生成記事を人間が確認
- 良さそうな記事をnote投稿候補にする
- 低品質記事を改善
- 需要が弱いジャンルを調整
- YouTubeキーワードを更新
- 禁止表現リストを更新
```

### 18.3 月次

```text
- 3ジャンルの成果を比較
- 記事在庫数を確認
- note投稿済み記事があれば売上CSVを分析
- 価格帯を見直す
- 新しいMCP/Skill/Plugin候補を評価
- AGENTS.mdを改善
```

---

## 19. 将来フェーズ

### 19.1 投稿システム

将来的に別システムとして作る。

候補:

```text
- BrowserMCPでnote編集画面に転記
- assisted_publish: 公開直前で停止
- auto_publish: 低リスク記事のみ、自動公開
```

ただし現フェーズでは実装しない。

### 19.2 売上分析システム

note販売履歴CSVを読み込んで分析する。

分析項目:

```text
- 記事別売上
- ジャンル別売上
- 価格別成約率
- 無料部分の長さと売上の関係
- 有料部分テンプレート有無と売上の関係
- YouTube由来テーマの売上
```

### 19.3 メンバーシップ / マガジン展開

記事在庫が増えたら、以下を検討する。

```text
- 有料マガジン
- メンバーシップ
- テンプレート集
- 実験ログシリーズ
- Google Docsテンプレート配布
```

---

## 20. 重要な安全ルール

Codexは以下を絶対に守る。

```text
- noteへ投稿しない
- noteへログインしない
- note非公式APIを使わない
- Cookieを扱わない
- パスワードを扱わない
- YouTube字幕全文を保存しない
- 人気動画の要約だけを販売記事にしない
- 誇大広告を書かない
- 投資・医療・法律を断定しない
- 認証情報をGitに保存しない
- 時間外に通常実行しない
- 同じ記事を重複作成しない
- ツール追加時は必ずログを残す
```

---

## 21. 参考ソース

以下は、このシステム設計時点で参照した公式・信頼ソースである。Codexは仕様変更の可能性がある情報について、必要に応じて最新情報を確認すること。

### Codex / OpenAI

- Codex Best Practices: https://developers.openai.com/codex/learn/best-practices
- AGENTS.md Guide: https://developers.openai.com/codex/guides/agents-md
- Codex Customization: https://developers.openai.com/codex/concepts/customization
- Codex Skills: https://developers.openai.com/codex/skills
- Codex Subagents: https://developers.openai.com/codex/subagents
- Codex Automations: https://developers.openai.com/codex/app/automations
- Codex Config Reference: https://developers.openai.com/codex/config-reference

### Google / YouTube

- Google Drive API — Create folders: https://developers.google.com/workspace/drive/api/guides/folder
- Google Drive MIME types: https://developers.google.com/workspace/drive/api/guides/mime-types
- Google Docs API — documents.batchUpdate: https://developers.google.com/workspace/docs/api/reference/rest/v1/documents/batchUpdate
- YouTube Data API — search.list: https://developers.google.com/youtube/v3/docs/search/list
- YouTube Data API — videos.list: https://developers.google.com/youtube/v3/docs/videos/list
- YouTube API Services Developer Policies: https://developers.google.com/youtube/terms/developer-policies
- Google Workspace MCP servers: https://developers.google.com/workspace/guides/configure-mcp-servers

### BrowserMCP

- BrowserMCP Docs: https://docs.browsermcp.io/
- BrowserMCP Server Setup: https://docs.browsermcp.io/setup-server
- BrowserMCP Extension Setup: https://docs.browsermcp.io/setup-extension

### GitHub Actions

- GitHub Actions workflow syntax / schedule: https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions

### note

- note公式公開APIについて: https://www.help-note.com/hc/ja/articles/46643492548121
- 有料記事を書く / 有料ライン設定: https://www.help-note.com/hc/ja/articles/360008882894
- コンテンツ販売時の手数料: https://www.help-note.com/hc/ja/articles/360011358873
- note販売履歴CSVエクスポート: https://www.help-note.com/hc/ja/articles/35228036879257
- note AIアシスタント利用条件: https://www.help-note.com/hc/ja/articles/15386417475481
- note利用規約: https://terms.help-note.com/hc/ja/articles/44943817565465

---

## 22. 最終確認

このシステムの本質は、以下である。

```text
投稿自動化ではなく、記事在庫の自動生成。
YouTube要約ではなく、需要発見と独自価値化。
AI丸投げではなく、検証ログ・テンプレート・実装手順の商品化。
完全放置ではなく、朝だけ動く制御された自律運用。
ツール固定ではなく、安全基準を満たすツールを自律追加して改善し続ける仕組み。
```

Codexは、毎回この思想に沿って作業すること。
