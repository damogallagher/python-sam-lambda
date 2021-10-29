from shared.shared import get_cloudwatch_metrics


def lambda_handler(event, context):
    namespace = 'SageMaker'
    endpointName = 'sagemaker-soln-ddf-js-b4jav4-demo-endpoint'
    variantName = 'sagemaker-soln-ddf-js-b4jav4-demo-model'

    queryStringParameters = event["queryStringParameters"]
    metricName = queryStringParameters['metricName'] if 'metricName' in queryStringParameters else 'Invocations'
    dimensions = []

    if metricName in ['InvocationsPerInstance', 'Invocations']:
        dimensions = [{"Name": "EndpointName", "Value": endpointName }, {"Name": "VariantName", "Value": variantName }]
    else:
        dimensions = [{"Name": "EndpointName", "Value": endpointName }, {"Name": "VariantName", "Value": variantName }]

    return get_cloudwatch_metrics(namespace, metricName, dimensions, event)
