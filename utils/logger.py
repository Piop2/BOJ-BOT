"""
# LOGGER
- root ( ~ INFO )
# COMMAND LOGGER
- cmd.problem ( ~ INFO ): /problem
"""

import logging
import logging.config
import json

LOG_CONFIG_PATH = "data/log_format.json"

with open(LOG_CONFIG_PATH, "r") as f:
    config = json.load(f)

logging.config.dictConfig(config)


def get_logger(name: str = None) -> logging.Logger:
    """
    get name of logger
    """
    return logging.getLogger(name)
