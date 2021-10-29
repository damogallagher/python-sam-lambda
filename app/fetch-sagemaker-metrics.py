from shared.shared import get_cloudwatch_metrics

# Get SageMaker Metrics
# Pass in metric you want as a query param named metricName
# Note: for https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html#cloudwatch-metrics-jobs see fetch-custom-sagemaker-metrics.py
# For https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html#cloudwatch-metrics-ground-truth, https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html#cloudwatch-metrics-feature-store and https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html#cloudwatch-metrics-pipelines - these have not been added as of yet
def lambda_handler(event, context):
    namespace = 'AWS/SageMaker'
    endpointName = 'sagemaker-soln-ddf-js-b4jav4-demo-endpoint'
    variantName = 'sagemaker-soln-ddf-js-b4jav4-demo-model'

    queryStringParameters = event["queryStringParameters"]
    metricName = queryStringParameters['metricName'] if 'metricName' in queryStringParameters else 'Invocations'
    dimensions = []

    #Endpoint Invocation metrics - https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html#cloudwatch-metrics-endpoint-invocation
    if metricName in ['Invocation4XXErrors', 'Invocation5XXErrors', 'Invocations', 'InvocationsPerInstance', 'ModelLatency', 'OverheadLatency']:
        dimensions = [{"Name": "EndpointName", "Value": endpointName }, {"Name": "VariantName", "Value": variantName }]
    #Multi-Model Endpoint metrics - https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html#cloudwatch-metrics-multimodel-endpoints
    elif metricName in ['ModelLoadingWaitTime', 'ModelUnloadingTime', 'ModelDownloadingTime', 'ModelLoadingTime', 'ModelCacheHit']:
        dimensions = [{"Name": "EndpointName", "Value": endpointName }, {"Name": "VariantName", "Value": variantName }]              
    else:
        dimensions = [{"Name": "EndpointName", "Value": endpointName }, {"Name": "VariantName", "Value": variantName }]

    return get_cloudwatch_metrics(namespace, metricName, dimensions, event)
