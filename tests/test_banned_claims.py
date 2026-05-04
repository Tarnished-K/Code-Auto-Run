from src.banned_claims import find_banned_claims


def test_detects_banned_claims() -> None:
    assert "必ず稼げる" in find_banned_claims("この方法なら必ず稼げると断定する")


def test_safe_expression_is_not_overdetected() -> None:
    assert find_banned_claims("自分の環境ではこう動いた実験ログです") == []
