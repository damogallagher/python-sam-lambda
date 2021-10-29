import boto3
from botocore.config import Config
import json
from datetime import date, timedelta, datetime

def get_cloudwatch_metrics_event(event):
    queryStringParameters = event["queryStringParameters"]
    if 'namespace' not in queryStringParameters or 'metricName' not in queryStringParameters:
        return 'bad request! Namespace or metricName are not specified', 400

    namespace = queryStringParameters['namespace']
    metricName = queryStringParameters['metricName']        
    dimensions = json.loads(event["body"])
    return get_cloudwatch_metrics(namespace, metricName, dimensions, event)

def get_cloudwatch_metrics(namespace, metricName, dimensions, event):
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
    queryStringParameters = event["queryStringParameters"]

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

    my_config = Config(
        region_name = 'us-east-1',
        signature_version = 'v4',
        retries = {
            'max_attempts': 10,
            'mode': 'standard'
        }
    )

    client = boto3.client('cloudwatch', config=my_config)
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

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        "body": json.dumps(response, indent=4, sort_keys=False, default=str),
    }
