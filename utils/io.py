import json
from pathlib import Path


def save_json(data, path: str):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_json(path: str):
    with open(path, "r") as f:
        return json.load(f)


def exists(path: str) -> bool:
    return Path(path).exists()


def mark_done(stage_dir: str):
    Path(stage_dir, ".done").touch()


def is_done(stage_dir: str) -> bool:
    return Path(stage_dir, ".done").exists()