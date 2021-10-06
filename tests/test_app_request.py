import pytest, json, os, requests
from urllib.parse import urljoin
from .config import dynamo_db_chaos
from thundra_demo_localstack.utils import execute_command

api_gateway_url = None

@pytest.fixture(scope="module", autouse=True)
def module_fixture():
    global api_gateway_url
    execute_command(
        "make deploy",
        {
            "env": {
                "THUNDRA_DYNAMODB_CHAOS": json.dumps(dynamo_db_chaos),
                **os.environ
            }
        }
    )
    result_raw = execute_command('awslocal apigateway get-rest-apis')
    if result_raw and result_raw.stdout:
        result = json.loads(result_raw.stdout)
        if result and "items" in result:
            rest_api_id = result.get("items")[0].get("id")
            api_gateway_url = f"http://localhost:4566/restapis/{rest_api_id}/local/_user_request_"
    yield
    res = execute_command('docker ps -a -q --filter ancestor=localstack/localstack --format="{{.ID}}"')
    localstack_container_id = json.loads(res.stdout)
    execute_command(f"docker stop {localstack_container_id}")

def test_create_request():
    try:
        global api_gateway_url
        create_request_url = api_gateway_url + '/requests'
        create_request_result = requests.post(create_request_url, {})
        data = json.loads(create_request_result.text)
        request_id = data.get("requestId")
        get_request_url = api_gateway_url + f"/request/{request_id}"
        get_request_result = requests.get(get_request_url)
    except Exception as e:
        print("test_create_request error: ", e)