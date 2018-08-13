"""
 Copyright (c) 2018 MeteoGroup Deutschland GmbH

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
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

