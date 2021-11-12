import boto3
from botocore.config import Config
import os
import opsgenie_sdk
from common_code import  boto3_client 

def get_value_from_parameter_store(parameter_name):
    client = boto3_client('ssm')
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

