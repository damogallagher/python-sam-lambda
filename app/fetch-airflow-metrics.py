from shared.shared import get_cloudwatch_metrics


def lambda_handler(event, context):
    namespace = 'AmazonMWAA'

    queryStringParameters = event["queryStringParameters"]
    metricName = queryStringParameters['metricName'] if 'metricName' in queryStringParameters else 'SchedulerHeartbeat'
    dimensions = []

    if metricName in ['PoolRunningSlots', 'PoolQueuedSlots', 'PoolOpenSlots']:
        dimensions = [{"Name": "Pool", "Value": "default_pool" }]
    elif metricName in ['OrphanedTasksCleared', 'CriticalSectionBusy', 'SchedulerHeartbeat', 'CriticalSectionDuration', 'OrphanedTasksAdopted']: 
        dimensions = [{"Name": "Function", "Value": "Scheduler" }]
    elif metricName in ['RunningTasks', 'OpenSlots', 'QueuedTasks']: 
        dimensions = [{"Name": "Function", "Value": "Executor" }]        
    elif metricName in ['ImportErrors', 'TotalParseTime', 'DagBagSize']: 
        dimensions = [{"Name": "Function", "Value": "DAG Processing" }] 
    else:
        dimensions = [{"Name": "Function", "Value": "Scheduler" }]

    dimensions.append({"Name": "Environment", "Value": "csx-nonprod-dataops"})

    return get_cloudwatch_metrics(namespace, metricName, dimensions, event)
