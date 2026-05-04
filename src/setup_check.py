from __future__ import annotations

import importlib.util
import os
from pathlib import Path

from src.env_loader import load_dotenv


REQUIRED_MODULES = (
    "googleapiclient",
    "google_auth_oauthlib",
    "google.oauth2.credentials",
    "openai",
)


def main() -> int:
    load_dotenv()
    client_path = Path(
        os.environ.get(
            "GOOGLE_OAUTH_CLIENT_PATH",
            os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "secrets/google_oauth_client.json"),
        )
    )
    token_path = Path(os.environ.get("GOOGLE_OAUTH_TOKEN_PATH", "secrets/google_oauth_token.json"))
    dry_run = os.environ.get("CODE_AUTO_RUN_DRY_RUN", "true").lower() != "false"
    use_ai = os.environ.get("CODE_AUTO_RUN_USE_AI", "false").lower() == "true"
    openai_model = os.environ.get("OPENAI_MODEL", "gpt-5.5")

    ok = True
    print("Code Auto Run setup check")
    print(f"- dry_run: {dry_run}")
    print(f"- use_ai: {use_ai}")
    print(f"- OpenAI model: {openai_model}")
    print(f"- OAuth client path: {client_path}")
    print(f"- OAuth token path: {token_path}")

    for module in REQUIRED_MODULES:
        found = importlib.util.find_spec(module) is not None
        print(f"- module {module}: {'ok' if found else 'missing'}")
        ok = ok and found

    client_exists = client_path.exists()
    token_exists = token_path.exists()
    print(f"- OAuth client JSON: {'ok' if client_exists else 'missing'}")
    print(
        "- OAuth token JSON: "
        f"{'ok' if token_exists else 'missing; run python -m src.google_auth_setup after adding client JSON'}"
    )

    if not client_exists:
        ok = False
        print("")
        print("Next action:")
        print("1. Enable Google Drive API and Google Docs API in Google Cloud Console.")
        print("2. Create an OAuth desktop client JSON.")
        print(f"3. Save it as: {client_path}")
        print("4. Run: python -m src.google_auth_setup")
    elif not token_exists:
        ok = False
        print("")
        print("Next action:")
        print("Run: python -m src.google_auth_setup")

    if use_ai and not os.environ.get("OPENAI_API_KEY"):
        ok = False
        print("")
        print("OpenAI API key is missing.")
        print("Set OPENAI_API_KEY before enabling CODE_AUTO_RUN_USE_AI=true.")

    if ok:
        print("")
        print("Setup looks ready. For live writes, set CODE_AUTO_RUN_DRY_RUN=false.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
