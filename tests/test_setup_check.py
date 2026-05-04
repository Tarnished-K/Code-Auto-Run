from src import setup_check


def test_setup_check_reports_missing_client(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)

    assert setup_check.main() == 1
    captured = capsys.readouterr()
    assert "OAuth client JSON: missing" in captured.out
    assert "python -m src.google_auth_setup" in captured.out
