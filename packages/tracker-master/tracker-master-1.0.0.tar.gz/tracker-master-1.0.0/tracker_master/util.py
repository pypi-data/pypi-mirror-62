import logging
import logging.config
import os
import json


def setup_logging(default_path='tracker_master/logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    # Setup logging configuration
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

class Util:

    def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
        # Setup logging configuration
        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)

        return logging.getLogger(__name__)