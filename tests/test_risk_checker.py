from src.risk_checker import assess_risk


def test_high_risk_terms_require_review() -> None:
    result = assess_risk("投資について断定する記事")
    assert result.level == "high"
    assert result.status == "needs_review"


def test_low_risk_article_can_be_stock_draft() -> None:
    result = assess_risk("Google Docsテンプレートの実験ログ")
    assert result.level == "low"
    assert result.status == "stock_draft"
