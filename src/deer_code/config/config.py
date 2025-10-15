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


def get_config_section(key: str) -> dict:
    global __config
    return __config[key]


load_config()
