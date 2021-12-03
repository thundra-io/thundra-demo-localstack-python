from .dynamodb import DynamoDbClient
from .s3 import S3Client
from .sns import SnsClient
from .sqs import SqsClient

dynamo_db_client = DynamoDbClient().dynamodbClient
s3_client = S3Client().s3_client
sns_client = SnsClient().sns_client
sqs_client = SqsClient().sqs_client

__all__ = [
    "dynamo_db_client",
    "s3_client",
    "sns_client",
    "sqs_client"
]