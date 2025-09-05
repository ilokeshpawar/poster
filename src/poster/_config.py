from pathlib import Path
from tomllib import load as toml_load


def load_config(config_path: Path) -> dict:
    """Load configuration from a TOML file."""
    with config_path.open("rb") as f:
        config = toml_load(f)
    return config


config = load_config(Path("config/config.toml"))
