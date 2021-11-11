import json
from shared_sagemaker import success_response, error_response, sagemaker_runtime_client

client = sagemaker_runtime_client()

# Invoke Sagemaker Endpoint
# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.invoke_endpoint
def lambda_handler(event, context):
    
    queryStringParameters = event["queryStringParameters"]
    if not queryStringParameters or 'endpoint' not in queryStringParameters :
        return error_response("endpoint is not specified")               

    endpoint = queryStringParameters['endpoint']


    #   response = client.invoke_endpoint(EndpointName=endpoint, Body=b'bytes') 

    custom_attributes = "c000b4f9-df62-4c85-a0bf-7c525f9104a4"  # An example of a trace ID.
    endpoint_name = endpoint                                       # Your endpoint name.
    content_type = "application/json"                                        # The MIME type of the input data in the request body.
    accept = "application/json"                                              # The desired MIME type of the inference in the response.
    payload = b'{"instances": "string of text"}'                                            # Payload for inference.
    response = client.invoke_endpoint(
        EndpointName=endpoint_name, 
        CustomAttributes=custom_attributes, 
        ContentType=content_type,
        Accept=accept,
        Body=payload
        )
        
    print("response:", response)
    print(response['CustomAttributes'])                         # If model receives and updates the custom_attributes header 
                                                            # by adding "Trace id: " in front of custom_attributes in the request,
                                                            # custom_attributes in response becomes
                                                            # "Trace ID: c000b4f9-df62-4c85-a0bf-7c525f9104a4"



    return success_response(json.dumps(response, indent=4, sort_keys=False, default=str))
