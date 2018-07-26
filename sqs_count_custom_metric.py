import logging
import os
import time

import boto3

from log.LoggingInitializer import LoggingInitializer


def main():
    LoggingInitializer.setup_once()
    log_level = os.getenv("LOG_LEVEL", logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    wait_time_in_seconds = int(os.getenv("WAIT_TIME_IN_SECONDS", 10))
    queue_name = os.getenv("QUEUE_NAME")
    environment = os.getenv("ENVIRONMENT") \
        or os.getenv('stage') \
        or os.getenv('env')
    namespace = os.getenv("METRICS_NAMESPACE")

    logger.info("Starting up with "
                "WAIT_TIME_IN_SECONDS: {} | "
                "QUEUE_NAME: {} | "
                "ENVIRONMENT: {} | "
                "METRICS_NAMESPACE: {}".format(
                    wait_time_in_seconds,
                    queue_name,
                    environment,
                    namespace
    ))

    while True:
        try:
            sqs_count_custom_metric(queue_name, environment,
                                    namespace, log_level)
        except Exception as e:
            logger.error(str(e))
        time.sleep(wait_time_in_seconds)


def sqs_count_custom_metric(queue_name, environment, namespace, log_level):
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
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    logger.debug("Sent another probe to {}: "
                 "ApproximateNumberOfMessages = {}"
                 .format(namespace, msg_count))
    return msg_count


if __name__ == '__main__':
    main()
