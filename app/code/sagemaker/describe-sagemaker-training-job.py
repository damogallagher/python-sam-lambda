import json
from common_code import  boto3_client, error_response, success_response

client = boto3_client('sagemaker')

# Describe Sagemaker training jobs
# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.describe_training_job
def lambda_handler(event, context):
    
    queryStringParameters = event["queryStringParameters"]
    if not queryStringParameters or 'trainingJobName' not in queryStringParameters :
        return error_response("TrainingJobName is not specified")               

    trainingJobName = queryStringParameters['trainingJobName']

    response = client.describe_training_job(TrainingJobName=trainingJobName)   
    print("Response:", response)
    return success_response(json.dumps(response, indent=4, sort_keys=False, default=str))
