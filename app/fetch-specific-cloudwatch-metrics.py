import boto3
import json
from datetime import date, timedelta, datetime


# import requests


def lambda_handler(event, context):
    days = 0
    yesterday=date.today() - timedelta(days=days)
    tomorrow=date.today() + timedelta(days=1)

    client = boto3.client('cloudwatch')
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'getSpecificMetricData',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AmazonMWAA',
                        'MetricName': 'SchedulerHeartbeat',
                        'Dimensions': [
                            {
                              "Name": "Function",
                              "Value": "Scheduler"
                            },
                            {
                              "Name": "Environment",
                              "Value": "csx-nonprod-dataops"
                            },
                        ]
                    },
                    'Period': 60 * 60,
                    'Stat': 'Sum',
                  },
                'Label': 'human-label',
                'ReturnData': True,
            },
        ],
        StartTime=datetime(yesterday.year, yesterday.month, yesterday.day), 
        EndTime=datetime(tomorrow.year, tomorrow.month, tomorrow.day),
        ScanBy='TimestampDescending',
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
