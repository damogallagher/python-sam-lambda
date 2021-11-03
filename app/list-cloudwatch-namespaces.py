import boto3
from botocore.config import Config
import json
from shared.shared import success_response, cloudwatch_client

# List Cloudwatch Namespaces
# List all the namespaces currently published in cloudwatch metrics
# See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-metrics.html
def lambda_handler(event, context):
    client = cloudwatch_client()
    namespaces_set = set()
    # List metrics through the pagination interface
    paginator = client.get_paginator('list_metrics')
    for response in paginator.paginate():
        for metric in response['Metrics']:
            namespaces_set.add(metric['Namespace'])
    
    return success_response(json.dumps(sorted(namespaces_set), indent=4, sort_keys=False, default=str))
