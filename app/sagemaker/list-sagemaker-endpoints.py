import json
from common_code import  boto3_client, success_response

client = boto3_client('sagemaker')

# List Sagemaker Endpoints
# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Paginator.ListEndpoints
def lambda_handler(event, context):
    
    paginator = client.get_paginator('list_endpoints')
    endpoints = []
    for response in paginator.paginate():
        for endpoint in response['Endpoints']:
            endpoint_dict = {}
            endpoint_dict['endpoint_name'] = endpoint['EndpointName']
            endpoint_dict['endpoint_arn'] = endpoint['EndpointArn']
            endpoint_dict['creation_time'] = endpoint['CreationTime']
            endpoint_dict['last_modified_time'] = endpoint['LastModifiedTime']
            endpoint_dict['endpoint_status'] = endpoint['EndpointStatus']
            endpoints.append(endpoint_dict)  
    
    return success_response(json.dumps(endpoints, indent=4, sort_keys=False, default=str))
