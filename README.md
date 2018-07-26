# sqs-count-custom-metric

Small service for creating a custom metric of high temporal resolution
for ApproximateNumberOfMessages in an SQS queue.

This can be very handy for fast scaling as per default,
the respective CloudWatch metric has a 5min resolution only.

See also https://aws.amazon.com/blogs/aws/auto-scaling-with-sqs/

Running this service will incur costs!

## Setup
1. Adjust Makefile to suit your docker registry
1. If you happen to not build with Bamboo,
   adjust the push scenario in Makefile
1. Create a version.txt file if you want custom tagging.
   The format is ``version=<version-tag>`` and the default created
   one is a timestamp.
1. ``make docker-build && make docker-push``
1. Run container. Default scenario is as a service in ECS, YMMV.
   You will need to provide permissions for reading the queue attributes
   and writing metrics, preferably by assuming a role
   in the execution environment.
1. Make use of the metrics!

## Customization

The following environment variables will get used
when a container is run:

| env variable | purpose | 
| ------------ | ------- |
| WAIT_TIME_IN_SECONDS | This is the wait time inbetween subsequent calls to the queue and defines the resolution of the metric. 10s = roughly 6 datapoints per minute, but beware of the runtime of queue-attribute poll and metrics push. |
| QUEUE_NAME | The queue in question. This will show up as dimension ``QueueName`` in the metrics |
| ENVIRONMENT | This will show up as dimension ``env`` in the metrics and supports different metrics for dev, prod and other stages |
| METRICS_NAMESPACE|Namespace for the custom metrics. |
| LOG_LEVEL | Default is ``INFO``, ``DEBUG`` will emit a message each loop |
| LOG_FORMAT | Default is plaintext, ``json`` will emit JSON which might be handy for a log aggregator. There are quite a few other environment variables picked up for logging, which might need to get adjusted in the code if desired. | 