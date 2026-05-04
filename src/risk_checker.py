from __future__ import annotations

from dataclasses import dataclass

from src.banned_claims import find_banned_claims

HIGH_RISK_TERMS = ("法律", "税金", "投資", "医療", "薬機法", "仮想通貨", "金融商品")


@dataclass(frozen=True)
class RiskResult:
    level: str
    status: str
    reasons: tuple[str, ...]


def assess_risk(text: str) -> RiskResult:
    reasons: list[str] = []
    banned = find_banned_claims(text)
    if banned:
        reasons.append(f"禁止表現: {', '.join(banned)}")
    high_risk = [term for term in HIGH_RISK_TERMS if term in text]
    if high_risk:
        reasons.append(f"高リスク領域: {', '.join(high_risk)}")
    if high_risk:
        return RiskResult(level="high", status="needs_review", reasons=tuple(reasons))
    if banned:
        return RiskResult(level="medium", status="needs_review", reasons=tuple(reasons))
    return RiskResult(level="low", status="stock_draft", reasons=())
