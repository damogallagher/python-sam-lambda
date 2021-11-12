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
    
    t0 = "2016-01-01 00:00:00"
    data_length = 400
    num_ts = 200
    period = 24
    time_series = []
    freq = "H"
    prediction_length = 48
    for k in range(num_ts):
        level = 10 * np.random.rand()
        seas_amplitude = (0.1 + 0.3 * np.random.rand()) * level
        sig = 0.05 * level  # noise parameter (constant in time)
        time_ticks = np.array(range(data_length))
        source = level + seas_amplitude * np.sin(time_ticks * (2 * np.pi) / period)
        noise = sig * np.random.randn(data_length)
        data = source + noise
        index = pd.date_range(start=t0, freq=freq, periods=data_length)
        time_series.append(pd.Series(data=data, index=index))

    queryStringParameters = event["queryStringParameters"]
    if not queryStringParameters or 'endpoint' not in queryStringParameters :
        return error_response("endpoint is not specified")               

    endpoint = queryStringParameters['endpoint']

    s3_bucket = "csx-sandbox"
    #s3_key = "csx_ts_data/od_m_vol_ATLANTA_ATLANTA (2).csv"
    s3_key = "csx_ts_data/od_m_vol_ATLANTA_CINCINNATI (1) (1).csv"
    s3_response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)

    # See https://towardsdatascience.com/reading-and-writing-files-from-to-amazon-s3-with-pandas-ccaf90bfe86c
    # Layers: https://towardsdatascience.com/python-packages-in-aws-lambda-made-easy-8fbc78520e30
    s3_status = s3_response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if s3_status == 200:
        time_series_training_df = pd.read_csv(s3_response.get("Body"))

        sagemaker_session = sagemaker.Session()
        role = get_execution_role()
        freq = "H"
        prediction_length = 48

        predictor = DeepARPredictor(endpoint_name=endpoint, sagemaker_session=sagemaker_session)

        predictor.set_prediction_parameters(freq, prediction_length)

        print("time_series_training_df:", time_series_training_df)
        print("time_series_training_df[:5]:", time_series_training_df[:5])
        print("time_series:", time_series)
        print("type(time_series_training_df):", type(time_series_training_df))
        print("type(time_series):", type(time_series))
        time_series_training_df_list = time_series_training_df.values.tolist()
        #list_of_df = predictor.predict(time_series[:5], content_type="application/json")
        list_of_df = predictor.predict(time_series_training_df_list[:5], content_type="application/json")
        print("list_of_df:", list_of_df)
        return success_response(json.dumps(time_series_training_df, indent=4, sort_keys=False, default=str))
    else:
        print(f"Unsuccessful S3 get_object response. Status - {s3_response}")
        return success_response("Hello world")

    #   response = sagemaker_runtime_client.invoke_endpoint(EndpointName=endpoint, Body=b'bytes') 

    ##custom_attributes = "c000b4f9-df62-4c85-a0bf-7c525f9104a4"  # An example of a trace ID.
    #endpoint_name = endpoint                                       # Your endpoint name.
    #content_type = "application/json"                                        # The MIME type of the input data in the request body.
    #accept = "application/json"                                              # The desired MIME type of the inference in the response.
    #payload = b'{"instances": "string of text"}'                                            # Payload for inference.
    #response = sagemaker_runtime_client.invoke_endpoint(
    #    EndpointName=endpoint_name, 
    #    CustomAttributes=custom_attributes, 
    #    ContentType=content_type,
    #    Accept=accept,
    #    Body=payload
    #    )
        
    #print("response:", response)
    #print(response['CustomAttributes'])                         # If model receives and updates the custom_attributes header 
                                                            # by adding "Trace id: " in front of custom_attributes in the request,
                                                            # custom_attributes in response becomes
                                                            # "Trace ID: c000b4f9-df62-4c85-a0bf-7c525f9104a4"



    #return success_response(json.dumps(response, indent=4, sort_keys=False, default=str))
