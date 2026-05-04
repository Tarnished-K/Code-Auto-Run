from __future__ import annotations

DISALLOWED_CATEGORIES = {
    "unofficial_note_api",
    "cookie_extractor",
    "captcha_bypass",
    "session_hijacking",
    "youtube_transcript_scraper_unofficial",
    "spam_automation_tool",
}


def evaluate_tool(category: str, score: int, external_write: bool = False) -> str:
    if category in DISALLOWED_CATEGORIES:
        return "rejected"
    if external_write:
        return "candidate_requires_permission_check"
    if score >= 85:
        return "added_candidate"
    if score >= 70:
        return "candidate"
    return "rejected"
