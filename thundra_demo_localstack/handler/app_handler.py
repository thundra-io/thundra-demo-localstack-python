from thundra_demo_localstack.service import start_new_request, list_requests_by_request_id
import json

headers = {
    "content-type": "application/json"
}

Handlers = {
    'POST/requests': start_new_request,
    'GET/request/{requestId}': list_requests_by_request_id
}

def generate_request_content(event, action):
    params = None
    result = None
    if ("pathParameters" in event):
        params = dict()
        params["pathParameters"] = event["pathParameters"]
    
    if not params:
        result = action()
    else:
        result = action(**params)
    return result

def handler(event, context):
    print("app-handler: ", event, context)
    resource = event["resource"]
    http_method = event["httpMethod"]
    handler_key = http_method + resource
    action = Handlers.get(handler_key, None)
    if not action:
        return {"statusCode": 404, "body": json.dumps({})}
    result = generate_request_content(event, action)
    return {
        "headers": headers,
        "statusCode": 200,
        "body": json.dumps(result)
    }