import boto3
import json
from datetime import date, timedelta, datetime


# import requests


def lambda_handler(event, context):
    print("Event")
    print(event)
    print(event["queryStringParameters"])
    print(event["queryStringParameters"])
    print("Context")
    print(context)
    if 'namespace' not in event["queryStringParameters"] or 'metricName' not in event["queryStringParameters"]:
      return 'bad request! Namespace or metricName are not specified', 400

    namespace = event["queryStringParameters"]['namespace'] 
    metricName = event["queryStringParameters"]['metricName']     
    period = int(event["queryStringParameters"]['period']) if 'period' in event["queryStringParameters"] else 60 
    stat = event["queryStringParameters"]['stat'] if 'stat' in event["queryStringParameters"] else 'Sum'      
    label = event["queryStringParameters"]['label'] if 'label' in event["queryStringParameters"] else 'label'  
    scanBy = event["queryStringParameters"]['scanBy'] if 'scanBy' in event["queryStringParameters"] else 'TimestampDescending'  
    previousDays = int(event["queryStringParameters"]['previousDays']) if 'previousDays' in event["queryStringParameters"] else 0  
    
    dimensions = json.loads(event["body"])

    yesterday=date.today() - timedelta(days=previousDays)
    tomorrow=date.today() + timedelta(days=1)

    client = boto3.client('cloudwatch')
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
