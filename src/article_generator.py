from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol

from src.article_format import ArticleDraft, format_article
from src.env_loader import load_dotenv


DEFAULT_OPENAI_MODEL = "gpt-5.5"


class ResponsesClient(Protocol):
    def create(self, **kwargs): ...


@dataclass(frozen=True)
class ArticleGenerationRequest:
    draft: ArticleDraft
    model: str = DEFAULT_OPENAI_MODEL


def generate_article_body(request: ArticleGenerationRequest, responses_client: ResponsesClient | None = None) -> str:
    load_dotenv()
    if os.environ.get("CODE_AUTO_RUN_USE_AI", "false").lower() != "true":
        return format_article(request.draft)

    client = responses_client or _build_openai_responses_client()
    response = client.create(
        model=request.model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "あなたはnote向けの実務記事編集者です。"
                            "人気動画の要約販売ではなく、独自の検証、手順、テンプレート、"
                            "失敗例、チェックリストに変換してください。"
                            "誇大表現、収益保証、note自動投稿、非公式API、Cookie利用は書かないでください。"
                            "必ず指定フォーマットのマーカーを独立段落として含めてください。"
                        ),
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": _build_prompt(request.draft),
                    }
                ],
            },
        ],
    )
    return _extract_response_text(response)


def _build_openai_responses_client() -> ResponsesClient:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("OpenAI SDK is missing. Run: python -m pip install -r requirements-dev.txt") from exc
    return OpenAI().responses


def _build_prompt(draft: ArticleDraft) -> str:
    skeleton = format_article(draft)
    return (
        "以下の記事フォーマットを保ったまま、本文を実用的なnote記事として拡充してください。\n"
        "無料部分は読者の悩み、結論、全体像を明確にしてください。\n"
        "有料部分は具体手順、検証ログ、テンプレート、プロンプト、設定例、失敗例、チェックリストを厚くしてください。\n"
        "出典欄と投稿前チェック欄は残してください。\n\n"
        f"{skeleton}"
    )


def _extract_response_text(response) -> str:
    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text
    output = getattr(response, "output", None) or []
    chunks: list[str] = []
    for item in output:
        content = getattr(item, "content", None) or []
        for part in content:
            text = getattr(part, "text", None)
            if text:
                chunks.append(text)
    if chunks:
        return "\n".join(chunks)
    raise RuntimeError("OpenAI response did not contain text output.")
