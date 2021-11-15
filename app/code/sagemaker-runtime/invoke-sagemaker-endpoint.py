from common_code import boto3_client, error_response, success_response
import pandas as pd
import numpy as np
import json
from DeepARPredictor import DeepARPredictor
import sagemaker
from sagemaker import get_execution_role

sagemaker_runtime_client = boto3_client('sagemaker-runtime')

# Invoke Sagemaker Endpoint
# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.invoke_endpoint
def lambda_handler(event, context):

    queryStringParameters = event["queryStringParameters"]
    if not queryStringParameters :
        return error_response("Query String Parameters are not specified")

    if 'endpoint' not in queryStringParameters:
        return error_response("endpoint is not specified")

    if 'od' not in queryStringParameters:
        return error_response("od is not specified")

    endpoint = queryStringParameters['endpoint']
    od = queryStringParameters['od']  

    bucket = "csx-sandbox"
    file_key = "csx_ts_data/od_m_vol_ATLANTA_ATLANTA (2).csv"
    s3uri = 's3://{}/{}'.format(bucket, file_key)
    df = pd.read_csv(s3uri)
    print("df 2:", df)

    df_to_forecast = df[df["od"] == od][["yr_mo", "od_y"]]
    print("df_to_forecast 1:", df_to_forecast)

    sagemaker_session = sagemaker.Session()
    #role = get_execution_role()

    prediction_length = 30
    freq = "D"
    t0 = min(df_to_forecast["yr_mo"])
    data_length = df_to_forecast.shape[0]
    forecast_list = []
    data = df_to_forecast["od_y"].values
    index = pd.date_range(start=t0, freq=freq, periods=data_length)
    forecast_list.append(pd.Series(data=data, index=index))

    predictor = DeepARPredictor(endpoint_name=endpoint, sagemaker_session=sagemaker_session)
    predictor.set_prediction_parameters(freq, prediction_length)

    list_of_df = predictor.predict(forecast_list, content_type="application/json")
    print("list_of_df:", list_of_df)
    print("list_of_df:", type(list_of_df))
    return success_response(json.dumps(list_of_df, indent=4, sort_keys=False, default=str))

