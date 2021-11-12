from common_code import  boto3_client, boto3_s3_client, error_response, success_response
import pandas as pd
import json

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
    #s3_key = "csx_ts_data/od_m_vol_ATLANTA_ATLANTA (2).csv"
    s3_key = "csx_ts_data/od_m_vol_ATLANTA_CINCINNATI (1) (1).csv"
    print("s3_bucket:", s3_bucket)
    print("s3_key:", s3_key)
    s3_response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
    print("s3_response:", s3_response)

    # See https://towardsdatascience.com/reading-and-writing-files-from-to-amazon-s3-with-pandas-ccaf90bfe86c
    # Layers: https://towardsdatascience.com/python-packages-in-aws-lambda-made-easy-8fbc78520e30
    s3_status = s3_response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    print("s3_status:", s3_status)

    if s3_status == 200:
        print(f"Successful S3 get_object response. Status - {s3_status}")
        books_df = pd.read_csv(s3_response.get("Body"))
        print("books_df:", books_df)
        return success_response(json.dumps(books_df, indent=4, sort_keys=False, default=str))
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
