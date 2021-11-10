import boto3
from botocore.config import Config
import os
import opsgenie_sdk

def ssm_client():
    client_config = Config(
        region_name = os.environ['REGION_NAME'],
        signature_version = os.environ['SIGNATURE_VERSION'],
        retries = {
            'max_attempts': int(os.environ['RETRIES_MAX_ATTEMPTS']),
            'mode': os.environ['RETRIES_MODE']
        }
    )

    return boto3.client('ssm', config=client_config)

def get_value_from_parameter_store(parameter_name):
    client = ssm_client()
    parameter = client.get_parameter(Name=parameter_name, WithDecryption=True)
    return parameter['Parameter']['Value']

def get_alert_api():
    conf = opsgenie_sdk.configuration.Configuration()

    OPSGENIE_API_KEY_PARAM = os.environ['OPSGENIE_API_KEY_PARAM']
    OPSGENIE_API_KEY_VALUE = get_value_from_parameter_store(OPSGENIE_API_KEY_PARAM)

    conf.api_key['Authorization'] = OPSGENIE_API_KEY_VALUE

    api_client = opsgenie_sdk.api_client.ApiClient(configuration=conf)
    alert_api = opsgenie_sdk.AlertApi(api_client=api_client)
    return alert_api

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