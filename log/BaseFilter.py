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
