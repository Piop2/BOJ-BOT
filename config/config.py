"""
python
version is >= 3.11 -> tomllib
or <= 3.10 -> tomlkit ( pip install tomlkit )
"""


import tomllib
# import tomlkit

CONFIG_PATH = "config.toml"

with open(CONFIG_PATH, "rb") as f:
    conf = tomllib.load(f)

# with open(CONFIG_PATH, "r", encoding="UTF-8") as f:
#     conf = tomlkit.parse(f.read())
