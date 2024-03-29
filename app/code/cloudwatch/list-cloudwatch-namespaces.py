from common_code import  boto3_client, success_response
import json

client = boto3_client('cloudwatch')

# List Cloudwatch Namespaces
# List all the namespaces currently published in cloudwatch metrics
# See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-metrics.html
def lambda_handler(event, context):
    
    namespaces_set = set()
    # List metrics through the pagination interface
    paginator = client.get_paginator('list_metrics')
    for response in paginator.paginate():
        for metric in response['Metrics']:
            namespaces_set.add(metric['Namespace'])
    
    return success_response(json.dumps(sorted(namespaces_set), indent=4, sort_keys=False, default=str))
