from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

FREE_MARKER = "【無料部分ここから】"
PAID_LINE_MARKER = "【NOTE有料ライン候補：この段落の直後に有料ラインを設定】"
PAID_START_MARKER = "【有料部分ここから】"


@dataclass(frozen=True)
class ArticleDraft:
    title: str
    genre: str
    status: str = "stock_draft"
    created_on: date = field(default_factory=date.today)
    target_reader: str = "noteで使える実務記事の型を探している人"
    estimated_price: str = "980〜2,980円"
    sales_format: str = "note有料記事"
    risk_level: str = "low"
    quality_score: int = 80
    source_urls: tuple[str, ...] = ()
    youtube_video_ids: tuple[str, ...] = ()
    fingerprint: str = ""
    reader_pain: str = "AI活用や記事在庫化の手順が抽象論に寄り、実装に移しにくい。"
    paid_value: str = "そのまま使えるテンプレート、確認手順、失敗時の切り分け観点。"
    competitor_gap: str = "動画や一般記事では省かれがちな運用ルールと安全制御まで扱う。"
    unique_value: str = "実際のリポジトリ構成に落とし込める形式で整理する。"


def format_article(draft: ArticleDraft) -> str:
    sources = draft.source_urls or ("未設定",)
    videos = draft.youtube_video_ids or ("なし",)
    fingerprint = draft.fingerprint or "pending"
    return "\n".join(
        [
            f"# {draft.title}",
            "",
            "【管理メタデータ】",
            f"ジャンル: {draft.genre}",
            f"ステータス: {draft.status}",
            f"作成日: {draft.created_on.isoformat()}",
            f"想定読者: {draft.target_reader}",
            f"想定価格: {draft.estimated_price}",
            f"想定販売形式: {draft.sales_format}",
            f"リスクレベル: {draft.risk_level}",
            f"品質スコア: {draft.quality_score}",
            f"主要ソース: {', '.join(sources)}",
            f"YouTube参照動画: {', '.join(videos)}",
            f"記事フィンガープリント: {fingerprint}",
            "",
            "---",
            "",
            "【記事の狙い】",
            f"この記事が解決する悩み: {draft.reader_pain}",
            f"読者が有料部分で得るもの: {draft.paid_value}",
            f"競合との差分: {draft.competitor_gap}",
            f"独自価値: {draft.unique_value}",
            "",
            "---",
            "",
            FREE_MARKER,
            "",
            "## 導入",
            "AIや自動化の記事は、概念の説明だけでは実務に移しにくい。この記事では、記事在庫を作るために必要な構成と安全ルールを先に整理する。",
            "",
            "## 結論",
            "最初に作るべきものは投稿自動化ではなく、品質と重複を管理できる記事在庫の仕組みである。",
            "",
            "## なぜ今このテーマが重要か",
            "AIエージェントを使う作業は増えているが、認証情報、権利、誇大表現を制御しないまま自動化すると運用リスクが高い。",
            "",
            "## 全体像",
            "時間ガード、ジャンル設定、記事フォーマット、禁止表現チェック、重複チェック、台帳を小さく実装してから外部連携を足す。",
            "",
            "## 有料部分で扱う内容の予告",
            "有料部分では、実装手順、設定例、検証ログ、失敗例、チェックリストを扱う。",
            "",
            PAID_LINE_MARKER,
            "",
            PAID_START_MARKER,
            "",
            "## 具体手順",
            "1. AGENTS.mdで運用ルールを固定する。",
            "2. 設定ファイルでジャンル、禁止表現、稼働時間を管理する。",
            "3. 記事本文は無料部分と有料部分を必ず分ける。",
            "4. Google Docs保存前に品質、リスク、重複を検査する。",
            "",
            "## 実験ログ / 検証ログ",
            "- 時間外は通常実行を止め、設計・テストだけを許可する。",
            "- Google Docs連携はdry_runから始め、認証情報をGitに保存しない。",
            "",
            "## テンプレート",
            "- 管理メタデータ",
            "- 記事の狙い",
            "- 無料部分",
            "- 有料ライン候補",
            "- 有料部分",
            "- 参考ソース",
            "- 投稿前チェック",
            "",
            "## プロンプト",
            "この記事の目的、対象読者、有料部分に入れる具体物、禁止表現を先に指定してから草稿を生成する。",
            "",
            "## 設定ファイル例",
            "`config/runtime_window.yaml`、`config/genres.yaml`、`config/banned_claims.yaml` を分けて管理する。",
            "",
            "## 失敗例と対処法",
            "- 時間外に通常実行してしまう: runtime_window_guardで停止する。",
            "- 似た記事を作る: フィンガープリントで判定する。",
            "- 誇大表現が混ざる: banned_claimsで検出する。",
            "",
            "## チェックリスト",
            "- [ ] 無料部分だけでも価値がある",
            "- [ ] 有料部分に具体物がある",
            "- [ ] 参考ソースがある",
            "- [ ] 禁止表現がない",
            "",
            "## 応用例",
            "Google Workspace効率化、YouTubeリサーチ、AIエージェント実験ログの3ジャンルに同じ仕組みを使える。",
            "",
            "## まとめ",
            "記事在庫システムは、投稿前の品質管理と運用ログを作るための土台である。",
            "",
            "---",
            "",
            "【参考ソース】",
            *[f"- Source {index}: {source}" for index, source in enumerate(sources, start=1)],
            "",
            "---",
            "",
            "【投稿前チェック】",
            "- [ ] 盗作・剽窃ではない",
            "- [ ] YouTube動画の要約だけになっていない",
            "- [ ] 誇大表現がない",
            "- [ ] 「必ず儲かる」系表現がない",
            "- [ ] 事実情報に出典がある",
            "- [ ] 無料部分だけでも読者に価値がある",
            "- [ ] 有料部分に具体物がある",
            "- [ ] noteの有料ライン候補が独立段落になっている",
            "",
        ]
    )


def validate_article_format(text: str) -> list[str]:
    errors: list[str] = []
    for marker in (FREE_MARKER, PAID_LINE_MARKER, PAID_START_MARKER):
        if marker not in text.splitlines():
            errors.append(f"missing independent marker: {marker}")
    for required in ("【管理メタデータ】", "【記事の狙い】", "【参考ソース】", "【投稿前チェック】"):
        if required not in text:
            errors.append(f"missing section: {required}")
    return errors
