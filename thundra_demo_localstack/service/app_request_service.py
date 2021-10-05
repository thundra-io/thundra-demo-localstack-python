from thundra_demo_localstack.modules import dynamo_db_client, sns_client, s3_client, sqs_client
from thundra_demo_localstack.utils import generate_short_uuid, delay, get_current_time
from thundra_demo_localstack.constants import AppRequestItemStatus
from thundra_demo_localstack.config import EnvironmentConfig
import json

def add_app_request(request_id, status):

    def put_item_to_dynamodb(item):
        try:
            dynamo_db_client.put_item(
                TableName=EnvironmentConfig.APP_REQUESTS_TABLE_NAME,
                Item= item
            )
        except Exception as e:
            print("Error in put_item_to_dynamodb", e)

    item = {
        "requestId": {"S": f"${request_id}"},
        "timestamp": {"S": f"{get_current_time()}"},
        "status": {"S": f"{status}"}
    }
    put_item_to_dynamodb(item)


def get_app_request(request_id):
    
    def get_item_from_dynamodb():
        result = dynamo_db_client.get_item(
            TableName=EnvironmentConfig.APP_REQUESTS_TABLE_NAME,
            Key={
                "requestId": {
                    "S": f"{request_id}"
                }
            }
        )
        return result

    return get_item_from_dynamodb()

def send_app_request_notification(request_id):

    def publish_sns():
        sns_client.publish(
            TopicArn=EnvironmentConfig.REQUEST_TOPIC_ARN,
            Message=json.dumps({"requestId": request_id})
        )

    publish_sns()


def start_new_request():

    def sqs_send_message(params):
        sqs_client.send_message(**params)

    request_id = generate_short_uuid()
    params = {
        "MessageBody": json.dumps({"requestId": request_id}),
        "QueueUrl": EnvironmentConfig.REQUEST_QUEUE_URL,
    }
    
    sqs_send_message(params)
    status = AppRequestItemStatus.QUEUED
    add_app_request(request_id, status)
    
    return {"requestId": request_id, "status": status}

def list_requests_by_request_id(path_parameters=None, **opts):

    def handle_item(item):
        for attr in item.keys():
            attr_value = item[attr]
            if 'N' in attr_value:
                item[attr] = float(attr_value['N'])
            elif 'S' in attr_value:
                item[attr] = attr_value['S']
            else:
                item[attr] = attr_value[attr_value.keys()[0]]

    request_id = path_parameters.get("requestId", None)
    if not request_id:
        return
    result = get_app_request(request_id)
    item = result.get("Item", None)
    if not item:
        return
    handle_item(item)
    return item


def process_request(request_id):
    delay(4000)
    add_app_request(request_id, AppRequestItemStatus.PROCESSING)
    delay(5000)
    send_app_request_notification(request_id)


def archive_request(request_id):
    
    
    def s3_put_object(params):
        s3_client.put_object(**params)

    
    params = {
        "Bucket": EnvironmentConfig.ARCHIVE_BUCKET_NAME,
        "Key": f"/result.txt{request_id}",
        "Body": json.dumps({
            "context": f"Archive result for request {request_id}"
        }),
        "ContentType": "application/json"
    }
    s3_put_object(params)
    delay(3000)
    add_app_request(request_id, AppRequestItemStatus.FINISHED)