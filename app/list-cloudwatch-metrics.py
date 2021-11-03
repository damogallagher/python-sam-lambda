import boto3
from botocore.config import Config
import json
from shared.shared import error_response, success_response, cloudwatch_client

client = cloudwatch_client()

# List CloudWatch Metrics
# Pass in a namespace you want as a query param named namespace to get all metrics and dimensions for that namespace
# See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-metrics.html
def lambda_handler(event, context):
    
    queryStringParameters = event["queryStringParameters"]
    if not queryStringParameters or 'namespace' not in queryStringParameters :
        return error_response("Namespace is not specified")               

    namespace = queryStringParameters['namespace']
     
    metric_dict = {} 
    # List metrics through the pagination interface
    paginator = client.get_paginator('list_metrics')
    for response in paginator.paginate(Namespace=namespace):
        for metric in response['Metrics']:
            metric_name = metric['MetricName']
            dimensions = metric['Dimensions']
            if metric_name not in metric_dict:
                metric_dict[metric_name] = [dimensions]
            else:
                curr_dimensions = metric_dict[metric_name]
                curr_dimensions.append(dimensions)
                metric_dict[metric_name] = [curr_dimensions]
    print(metric_dict)

    return success_response(json.dumps(metric_dict))
