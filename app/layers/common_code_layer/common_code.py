import boto3
from botocore.config import Config
import os

#For working in layers - see https://aws.plainenglish.io/a-practical-guide-surviving-aws-sam-part-3-lambda-layers-8a55eb5d2cbe
def boto3_client(service_name):
    # Create CloudWatch client
    client_config = Config(
        region_name = os.environ['REGION_NAME'],
        signature_version = os.environ['SIGNATURE_VERSION'],
        retries = {
            'max_attempts': int(os.environ['RETRIES_MAX_ATTEMPTS']),
            'mode': os.environ['RETRIES_MODE']
        }
    )

    return boto3.client(service_name, config=client_config)

def error_response(message):
    print(message)
    return {
            "statusCode": 400,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            "body": message,
    } 

def success_response(body):
    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        "body": body,
    }