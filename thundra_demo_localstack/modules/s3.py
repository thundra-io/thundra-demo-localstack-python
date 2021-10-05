import boto3
from botocore.config import Config
from thundra_demo_localstack.utils import Singleton
from thundra_demo_localstack.config import EnvironmentConfig


class S3Client(metaclass=Singleton):

    def __init__(self, config_s3={"addressing_style": "path"}):
        self.s3_client = boto3.client('s3', 
            region_name=EnvironmentConfig.AWS_REGION, 
            endpoint_url=EnvironmentConfig.LOCALSTACK_URL,
            config=Config(s3=config_s3)
        )