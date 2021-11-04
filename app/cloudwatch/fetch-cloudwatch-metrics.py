from shared import error_response, success_response, cloudwatch_client
import json
import json
from datetime import date, timedelta, datetime

client = cloudwatch_client()

# Get Cloudwatch Metrics
# Pass in namespace you want as a query param named namespace
# Pass in metricName you want as a query param named metricName
# Pass in dimensions you want as the request body
def lambda_handler(event, context):

    queryStringParameters = event["queryStringParameters"]
    # if not queryStringParameters or 'namespace' not in queryStringParameters or 'metricName' not in queryStringParameters:
    #     return error_response("Namespace or metric name is not specified")               

    if not queryStringParameters:
        print(event)
        return error_response("No queryParams returned")     

    if 'namespace' not in queryStringParameters:
        print(event)
        return error_response("namespace is not specified")     

    if 'metricName' not in queryStringParameters:
        print(event)
        return error_response("metricName is not specified")     
        
    namespace = queryStringParameters['namespace']
    metricName = queryStringParameters['metricName']

    if not event or not event["body"]:
        return error_response("Request body is not specified. Please pass in the dimensions in the request body")     

    dimensions = json.loads(event["body"])
    print("Event")
    print(event)
    print("namespace")
    print(namespace)
    print("metricName")
    print(metricName)
    print("dimensions")
    print(dimensions)        
    print("queryStringParameters")
    print(event["queryStringParameters"])

    if not queryStringParameters:
        stat = 'Sum'
        label = 'label'
        scanBy = 'TimestampDescending'
        period = 60
        previousDays = 0        
    else:
        stat = queryStringParameters['stat'] if 'stat' in queryStringParameters else 'Sum'
        label = queryStringParameters['label'] if 'label' in queryStringParameters else 'label'
        scanBy = queryStringParameters['scanBy'] if 'scanBy' in queryStringParameters else 'TimestampDescending'
        period = int(queryStringParameters['period']) if 'period' in queryStringParameters else 60
        previousDays = int(queryStringParameters['previousDays']) if 'previousDays' in queryStringParameters else 0

    yesterday = date.today() - timedelta(days=previousDays)
    tomorrow = date.today() + timedelta(days=1)

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'getMetricData',
                'MetricStat': {
                    'Metric': {
                        'Namespace': namespace,
                        'MetricName': metricName,
                        'Dimensions': dimensions
                    },
                    'Period': period,
                    'Stat': stat,
                },
                'Label': label,
                'ReturnData': True,
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day),
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
        ScanBy=scanBy,
    )
    print(response)

    return success_response(json.dumps(response, indent=4, sort_keys=False, default=str))
