import boto3
from botocore.config import Config
import os

def sagemaker_client():
    return create_client('sagemaker')

def sagemaker_runtime_client():
    return create_client('sagemaker-runtime')

def create_client(service_name):
    # Create Sagemaker client based on service_name passed in
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