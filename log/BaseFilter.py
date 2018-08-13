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
import os
from logging import Filter


class BaseFilter(Filter):
    def __init__(self):
        super(BaseFilter, self).__init__()
        self.additional_fields = dict()
        for field in ('cluster', 'instance', 'application_name',
                      'application_version', 'stage', 'datatype_level_1',
                      'datatype_level_2', 'datatype_level_3'):
                self.additional_fields[field] = os.getenv(field, '')

    def filter(self, record):
        # Default implementation: do nothing
        return True
