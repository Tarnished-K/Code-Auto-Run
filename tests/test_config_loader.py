from src.config_loader import load_config


def test_loads_genres_config() -> None:
    config = load_config("config/genres.yaml")
    assert len(config["genres"]) == 3
    assert config["genres"][0]["id"] == "01"
