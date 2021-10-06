import pytest, json, os, requests
import time
from .config import dynamo_db_chaos
from thundra_demo_localstack.utils import execute_command
from thundra_demo_localstack.constants import AppRequestItemStatus

api_gateway_url = None

def eventually(get_request_url, deadline_in_sec = 10, task_run_freq_in_sec = 10):
    def check_result(get_request_url):
        create_request_result = requests.get(get_request_url)
        data = json.loads(create_request_result.text)
        res = (create_request_result and 
                data and 
                create_request_result.status_code == 200 and 
                data.get("status") == AppRequestItemStatus.FINISHED)
        return res

    deadline = int(time.time()) + deadline_in_sec
    print("deadline: ", deadline)
    expect_error = None
    res = False

    while(int(time.time()) < deadline):
        try:
            res = check_result(get_request_url)
            if res:
                break
        except Exception as e:
            expect_error = e
        time.sleep(task_run_freq_in_sec)
    
    if expect_error:
        raise expect_error

    return res

@pytest.fixture(scope="module", autouse=True)
def module_fixture():
    global api_gateway_url
    execute_command(
        "make deploy",
        {
            "env": {
                # "THUNDRA_DYNAMODB_CHAOS": json.dumps(dynamo_db_chaos),
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
    global api_gateway_url
    create_request_url = api_gateway_url + '/requests'
    create_request_result = requests.post(create_request_url, {})
    assert create_request_result
    assert create_request_result.text
    assert create_request_result.status_code == 200
    data = json.loads(create_request_result.text)
    request_id = data.get("requestId")
    assert request_id
    get_request_url = api_gateway_url + f"/request/{request_id}"
    res = eventually(get_request_url, 120, 20)
    assert res
    