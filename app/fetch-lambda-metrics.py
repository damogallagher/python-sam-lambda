from shared.shared import get_cloudwatch_metrics


def lambda_handler(event, context):
    namespace = 'Lambda'
    functionNameStr = 'FunctionName'
    resourceStr = 'Resource'

    queryStringParameters = event["queryStringParameters"]
    metricName = queryStringParameters['metricName'] if 'metricName' in queryStringParameters else 'Invocations'
    functionName = queryStringParameters['functionName'] if 'functionName' in queryStringParameters else 'functionName'
    dimensions = []

    if metricName in ['Invocations', 'Duration', 'Errors', 'Throttles', 'ConcurrentExecutions']:
        dimensions = [{"Name": functionNameStr, "Value": functionName },{"Name": resourceStr, "Value": functionName }]
    else:
        dimensions = [{"Name": functionNameStr, "Value": functionName },{"Name": resourceStr, "Value": functionName }]

    return get_cloudwatch_metrics(namespace, metricName, dimensions, event)
