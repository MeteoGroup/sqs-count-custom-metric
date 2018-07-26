from __future__ import absolute_import

from six import iteritems

from log.BaseFilter import BaseFilter


class PlaintextFilter(BaseFilter):

    def filter(self, record):
        for field, value in iteritems(self.additional_fields):
            setattr(record, field, value)
        return True
