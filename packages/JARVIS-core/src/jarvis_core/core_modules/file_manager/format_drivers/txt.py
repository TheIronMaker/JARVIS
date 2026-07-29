from pathlib import Path

format = ".txt"

def load(path: Path, config: dict=None):
    default_config = {
        "mode": "r",
        "encoding": "utf-8"
    }

    # Could improve this system | maybe:
    # from jarvis_core.utils.collections import deep_merge
    config = config or default_config

    with open(path, config["mode"], encoding=config["encoding"]) as f:
        return f.read()