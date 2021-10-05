from thundra_demo_localstack.service import process_request
import json
def handler(event, context):

    print("processing-handler: ", event, context)
    records = event.get("Records")
    for record in records:
        body = json.loads(record.get("body", "null"))
        if not body:
            continue
        request_id = record.get("requestId")
        process_request(request_id)