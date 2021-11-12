import json
from common_code import  boto3_client, success_response

client = boto3_client('sagemaker')

# List Sagemaker training jobs
# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.list_training_jobs
def lambda_handler(event, context):
    
    paginator = client.get_paginator('list_training_jobs')
    training_jobs = []
    for response in paginator.paginate():
        print("Response:", response)
        for trainingJobSummary in response['TrainingJobSummaries']:
            training_jobs.append(trainingJobSummary)        
    
    return success_response(json.dumps(training_jobs, indent=4, sort_keys=False, default=str))
