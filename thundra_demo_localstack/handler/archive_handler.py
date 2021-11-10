from thundra_demo_localstack.service import archive_request
import json
from thundra.plugins.trace.traceable import Traceable
@Traceable(trace_line_by_line=True, trace_local_variables=True, trace_lines_with_source=True)
def handler(event, context):
    records = event.get("Records", None)
    if not records:
        return
    for record in records:
        sns = record.get("Sns")
        sns_message = json.loads(sns.get("Message", "null"))
        if not sns_message:
            continue
        request_id = sns_message.get("requestId")
        archive_request(request_id)