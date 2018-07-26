import logging
import os
import sys
import time

import boto3


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] "
               "%(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout
    )
    logging.getLogger('boto').setLevel(logging.ERROR)
    logging.getLogger('boto3').setLevel(logging.ERROR)
    logging.getLogger('botocore').setLevel(logging.ERROR)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    wait_time_in_seconds = int(os.getenv("WAIT_TIME_IN_SECONDS", 10))
    queue_name = os.getenv("QUEUE_NAME")
    environment = os.getenv("ENVIRONMENT") \
        or os.getenv('stage') \
        or os.getenv('env')
    namespace = os.getenv("METRIC_NAMESPACE")

    while True:
        try:
            sqs_count_custom_metric(queue_name, environment, namespace)
        except Exception as e:
            logger.error(str(e))
        time.sleep(wait_time_in_seconds)


def sqs_count_custom_metric(queue_name, environment, namespace):
    sqs = boto3.resource('sqs')
    cloudwatch = boto3.client('cloudwatch')

    queue = sqs.get_queue_by_name(QueueName=queue_name)
    msg_count = queue.attributes.get('ApproximateNumberOfMessages')

    # Send to Custom SQS Metrics
    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'ApproximateNumberOfMessages',
                'Dimensions': [
                    {
                        'Name': 'QueueName',
                        'Value': queue_name
                    },
                    {
                        'Name': 'env',
                        'Value': environment
                    },

                ],
                'Unit': 'None',
                'Value': float(msg_count)
            },
        ],
        Namespace=namespace
    )
    logging.getLogger().debug("Sent another probe: "
                              "ApproximateNumberOfMessages = {}"
                              .format(msg_count))
    return msg_count


if __name__ == '__main__':
    main()
