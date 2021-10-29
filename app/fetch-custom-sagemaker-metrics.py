from shared.shared import get_cloudwatch_metrics

# Get SageMaker Custom Metrics 
# Pass in metric you want as a query param named metricName
# See See https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html#cloudwatch-metrics-jobs
def lambda_handler(event, context):
    namespace = '/aws/sagemaker/Endpoints'
    endpointName = 'sagemaker-soln-ddf-js-b4jav4-demo-endpoint'
    variantName = 'sagemaker-soln-ddf-js-b4jav4-demo-model'

    queryStringParameters = event["queryStringParameters"]
    metricName = queryStringParameters['metricName'] if 'metricName' in queryStringParameters else 'CPUUtilization'
    dimensions = []

    if metricName in ['CPUUtilization', 'MemoryUtilization', 'DiskUtilization']:
        dimensions = [{"Name": "EndpointName", "Value": endpointName }, {"Name": "VariantName", "Value": variantName }]
    else:
        dimensions = [{"Name": "EndpointName", "Value": endpointName }, {"Name": "VariantName", "Value": variantName }]

    return get_cloudwatch_metrics(namespace, metricName, dimensions, event)
