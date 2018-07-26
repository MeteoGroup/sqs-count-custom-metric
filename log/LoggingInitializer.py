import logging
import logging.config
import os

import yaml


class LoggingInitializer(object):

    setup_done = False

    @classmethod
    def setup_once(cls):
        if cls.setup_done:
            return
        log_format = os.getenv('LOG_FORMAT', 'plain')
        logging_config_file = 'logging-json.yaml' \
            if log_format.lower() == 'json' \
            else 'logging-plaintext.yaml'
        logging_config_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(logging_config_dir, logging_config_file)) as f:
            logging_config = yaml.load(f)

        logging.config.dictConfig(logging_config)
        cls.setup_done = True

