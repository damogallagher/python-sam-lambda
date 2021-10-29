from shared.shared import get_cloudwatch_metrics

def lambda_handler(event, context):
    namespace = 'AmazonMWAA'
    metricName = 'SchedulerHeartbeat'

    dimensions = [
        {
            "Name": "Function",
            "Value": "Scheduler"
        },
        {
            "Name": "Environment",
            "Value": "csx-nonprod-dataops"
        },
    ]

    return get_cloudwatch_metrics(namespace, metricName, dimensions, event)
