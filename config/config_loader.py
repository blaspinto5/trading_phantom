# config/config_loader.py

import yaml
from pathlib import Path


def load_config(filename="config.yaml") -> dict:
    base_path = Path(__file__).resolve().parent
    config_path = base_path / filename

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
