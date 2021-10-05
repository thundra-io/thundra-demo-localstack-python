import boto3
from botocore import endpoint
from thundra_demo_localstack.config import EnvironmentConfig
from thundra_demo_localstack.utils import Singleton


class SqsClient(metaclass=Singleton):

    def __init__(self):
        self.sqs_client = boto3.client("sqs", 
            region_name=EnvironmentConfig.AWS_REGION,
            endpoint_url=EnvironmentConfig.LOCALSTACK_URL
        )