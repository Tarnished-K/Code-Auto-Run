from types import SimpleNamespace

from src.article_format import ArticleDraft, FREE_MARKER, PAID_LINE_MARKER, PAID_START_MARKER
from src.article_generator import ArticleGenerationRequest, generate_article_body


class FakeResponses:
    def __init__(self) -> None:
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            output_text="\n".join(
                [
                    "# テスト記事",
                    "【管理メタデータ】",
                    "【記事の狙い】",
                    FREE_MARKER,
                    PAID_LINE_MARKER,
                    PAID_START_MARKER,
                    "【参考ソース】",
                    "【投稿前チェック】",
                ]
            )
        )


def test_generation_uses_requested_model(monkeypatch) -> None:
    monkeypatch.setenv("CODE_AUTO_RUN_USE_AI", "true")
    fake = FakeResponses()

    body = generate_article_body(
        ArticleGenerationRequest(
            draft=ArticleDraft(title="テスト記事", genre="01_AIエージェント_自動化_実験ログ"),
            model="gpt-5.5",
        ),
        responses_client=fake,
    )

    assert "【無料部分ここから】" in body
    assert fake.kwargs["model"] == "gpt-5.5"


def test_generation_falls_back_to_template_by_default(monkeypatch) -> None:
    monkeypatch.delenv("CODE_AUTO_RUN_USE_AI", raising=False)

    body = generate_article_body(
        ArticleGenerationRequest(
            draft=ArticleDraft(title="テスト記事", genre="01_AIエージェント_自動化_実験ログ"),
            model="gpt-5.5",
        )
    )

    assert "【管理メタデータ】" in body
