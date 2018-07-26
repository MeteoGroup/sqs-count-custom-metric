FROM python:3-alpine

RUN pip install --no-cache-dir boto3 pyaml python-json-logger

WORKDIR /opt/app
COPY . .
CMD ["python", "sqs_count_custom_metric.py"]
