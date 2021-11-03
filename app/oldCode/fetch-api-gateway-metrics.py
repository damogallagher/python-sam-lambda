from shared.shared import get_cloudwatch_metrics

# Get Api Gateway Metrics
# Pass in metric you want as a query param named metricName
# See https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-metrics-and-dimensions.html
def lambda_handler(event, context):
    namespace = 'AWS/ApiGateway'
    apiName = "sam-lambda"

    queryStringParameters = event["queryStringParameters"]
    metricName = queryStringParameters['metricName'] if 'metricName' in queryStringParameters else 'Count'

    dimensions = []

    if metricName in ['Latency', '5XXError', '4XXError', 'Count', 'IntegrationLatency', 'Latency', 'CacheHitCount', 'CacheMissCount']:
        dimensions = [{"Name": "ApiName", "Value": apiName }]
    else:
        dimensions = [{"Name": "ApiName", "Value": apiName }]

    return get_cloudwatch_metrics(namespace, metricName, dimensions, event)
