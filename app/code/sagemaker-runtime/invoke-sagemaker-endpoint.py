from common_code import  boto3_client, boto3_s3_client, error_response, success_response
import pandas as pd
import numpy as np
import json
from DeepARPredictor import DeepARPredictor
import sagemaker
from sagemaker import get_execution_role



sagemaker_runtime_client = boto3_client('sagemaker-runtime')
s3_client = boto3_s3_client()

# Invoke Sagemaker Endpoint
# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.invoke_endpoint
def lambda_handler(event, context):

    queryStringParameters = event["queryStringParameters"]
    if not queryStringParameters or 'endpoint' not in queryStringParameters :
        return error_response("endpoint is not specified")               

    endpoint = queryStringParameters['endpoint']

    s3_bucket = "csx-sandbox"
    s3_key = "csx_ts_data/od_m_vol_ATLANTA_CINCINNATI (1) (1).csv"
    s3_response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)

    s3_status = s3_response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if s3_status == 200:
        s3_body = s3_response.get("Body")
        print("s3_body 1:", s3_body)

        time_series_training_df = pd.read_csv(s3_body)
        print("time_series_training_df 1:", time_series_training_df)
        

        sagemaker_session = sagemaker.Session()
        role = get_execution_role()
        freq = "H"
        prediction_length = 48

        predictor = DeepARPredictor(endpoint_name=endpoint, sagemaker_session=sagemaker_session)

        predictor.set_prediction_parameters(freq, prediction_length)

        list_of_df = predictor.predict(time_series_training_df[:5], content_type="application/json")
        return success_response(json.dumps(time_series_training_df, indent=4, sort_keys=False, default=str))
    else:
        print(f"Unsuccessful S3 get_object response. Status - {s3_response}")
        return success_response("Hello world")


