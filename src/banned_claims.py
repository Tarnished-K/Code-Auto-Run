from __future__ import annotations

from pathlib import Path


DEFAULT_BANNED_CLAIMS = (
    "必ず稼げる",
    "誰でも稼げる",
    "放置で稼げる",
    "完全自動で収益確定",
    "月収保証",
    "再現性100%",
    "ノーリスク",
    "絶対成功",
    "確実に儲かる",
    "最短で確実に",
    "裏技で稼ぐ",
)


def load_banned_claims(path: str | Path | None = None) -> tuple[str, ...]:
    if path is None:
        return DEFAULT_BANNED_CLAIMS
    text = Path(path).read_text(encoding="utf-8")
    claims = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            claims.append(stripped[2:].strip('"'))
    return tuple(claims) or DEFAULT_BANNED_CLAIMS


def find_banned_claims(text: str, claims: tuple[str, ...] = DEFAULT_BANNED_CLAIMS) -> list[str]:
    return [claim for claim in claims if claim in text]
