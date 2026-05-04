from src.article_format import (
    PAID_LINE_MARKER,
    ArticleDraft,
    format_article,
    validate_article_format,
)


def test_article_contains_required_markers_and_metadata() -> None:
    text = format_article(ArticleDraft(title="テスト記事", genre="01_AIエージェント_自動化_実験ログ"))
    assert validate_article_format(text) == []
    assert "【管理メタデータ】" in text
    assert "【無料部分ここから】" in text
    assert "【有料部分ここから】" in text


def test_paid_line_marker_is_independent_paragraph() -> None:
    text = format_article(ArticleDraft(title="テスト記事", genre="01_AIエージェント_自動化_実験ログ"))
    assert PAID_LINE_MARKER in text.splitlines()
