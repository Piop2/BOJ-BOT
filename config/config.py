import tomllib

CONFIG_PATH = "config.toml"

with open(CONFIG_PATH, "rb") as f:
    conf = tomllib.load(f)
