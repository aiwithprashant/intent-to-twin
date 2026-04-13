import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        with open(self.config_path, "r") as f:
            return yaml.safe_load(f)

    def get(self, key: str, default=None):
        keys = key.split(".")
        value = self.data
        for k in keys:
            value = value.get(k, default)
            if value is None:
                return default
        return value

    def __getitem__(self, item):
        return self.data[item]