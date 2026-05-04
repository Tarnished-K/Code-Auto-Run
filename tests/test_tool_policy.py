from src.tool_discovery_agent import evaluate_tool


def test_rejects_disallowed_tool_category() -> None:
    assert evaluate_tool("cookie_extractor", 100) == "rejected"


def test_safe_local_tool_can_be_candidate() -> None:
    assert evaluate_tool("python_package", 85) == "added_candidate"


def test_external_write_requires_permission_check() -> None:
    assert evaluate_tool("google_api_client", 90, external_write=True) == "candidate_requires_permission_check"
