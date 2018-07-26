FROM python:3-alpine

RUN apk update && \
    pip install --no-cache-dir boto3 && \
    rm -f /var/cache/apk/*

WORKDIR /opt/app
COPY . .
CMD ["python", "sqs_count_custom_metric.py"]
