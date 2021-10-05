from urllib.parse import urlparse
import os

def _get_url(url):
    try:
        localstack_host_name = os.getenv("LOCALSTACK_HOSTNAME")
        if localstack_host_name:
            parsed_url = urlparse(url)
            url = parsed_url._replace(netloc=localstack_host_name).geturl()
        return url
    except Exception as e:
        print("Exception occurs in config.get_url", e)

def _get_localstack_url():
    try:
        localstack_hostname = os.getenv("LOCALSTACK_HOSTNAME")
        if localstack_hostname:
            return f"http://{localstack_hostname}:4566"
        return None
    except Exception as e:
        print("Exception occurs in get_localstack_url", e)


class EnvironmentConfig:
    AWS_REGION = os.getenv("AWS_REGION")
    REQUEST_QUEUE_URL = _get_url(os.getenv("REQUEST_QUEUE_URL"))
    LOCALSTACK_URL = _get_localstack_url()
    APP_REQUESTS_TABLE_NAME = os.getenv("APP_REQUESTS_TABLE_NAME")
    REQUEST_TOPIC_ARN = os.getenv("REQUEST_TOPIC_ARN")
    ARCHIVE_BUCKET_NAME = os.getenv("ARCHIVE_BUCKET_NAME")