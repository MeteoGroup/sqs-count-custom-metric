import socket

from six import iteritems

from .BaseFilter import BaseFilter

from urllib.request import urlopen


class JsonFilter(BaseFilter):

    hostname = None

    def filter(self, record):
        for field, value in iteritems(self.additional_fields):
            setattr(record, field, value)
        if not self.hostname:
            self.hostname = self.retrieve_hostname()
        record.hostname = self.retrieve_hostname()
        return True

    def retrieve_hostname(self):
        local_hostname = None
        try:
            # Metadata service
            # http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html#instancedata-data-categories
            # Should get the ec2 instance hostname in AWS
            local_hostname = \
                'HOST:{}'.format(
                    urlopen(
                        'http://169.254.169.254/latest/meta-data/hostname',
                        timeout=10
                    ).read()
                )
        except:
            # If Metadata service is not available,
            # get direct hostname of container as fallback
            local_hostname = 'CONTAINER:{}'.format(socket.gethostname())
        return local_hostname
