"""
python
version is >= 3.11 -> tomllib
or <= 3.10 -> tomlkit ( pip install tomlkit )
"""


from sys import version_info

CONFIG_PATH = "config.toml"

if version_info.minor >= 11:
    import tomllib

    with open(CONFIG_PATH, "rb") as f:
        conf = tomllib.load(f)

else:
    import tomlkit

    with open(CONFIG_PATH, "r", encoding="UTF-8") as f:
        conf = tomlkit.parse(f.read())
