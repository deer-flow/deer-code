import os

import yaml

__config = None


def load_config() -> dict:
    global __config
    if __config is None:
        if not os.path.exists("config.yaml"):
            raise FileNotFoundError("DeerCode's `config.yaml` file is not found")
        with open("config.yaml", "r") as f:
            __config = yaml.safe_load(f)
    return __config


def get_config_section(key: str | list[str]) -> dict:
    path = []
    if isinstance(key, str):
        path.append(key)
    else:
        path.extend(key)
    global __config
    section = __config
    for key in path:
        if key not in section:
            raise ValueError(f"The `{key}` section in `config.yaml` is not found")
        section = section[key]
    return section


load_config()
