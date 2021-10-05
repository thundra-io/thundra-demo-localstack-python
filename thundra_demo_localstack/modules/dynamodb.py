import boto3
from thundra_demo_localstack.utils import Singleton
from thundra_demo_localstack.config import EnvironmentConfig


class DynamoDbClient(metaclass=Singleton):

    def __init__(self):
        self.dynamodbClient = boto3.client('dynamodb', endpoint_url=EnvironmentConfig.LOCALSTACK_URL, region_name=EnvironmentConfig.AWS_REGION)