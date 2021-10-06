from thundra_demo_localstack.service import process_request
import json
def handler(event, context):
    records = event.get("Records")
    for record in records:
        body = json.loads(record.get("body", "null"))
        if not body:
            continue
        request_id = body.get("requestId")
        print("process handler: request_id", request_id)
        process_request(request_id)