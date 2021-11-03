from shared.shared import get_cloudwatch_metrics

# Get S3 Metrics
# Pass in metric you want as a query param named metricName
# Need to pass in S3 Bucket as a query param named bucketName
# See https://docs.aws.amazon.com/AmazonS3/latest/userguide/metrics-dimensions.html
# Question - should we pass in the storage types of the bucket?
def lambda_handler(event, context):
    namespace = 'AWS/S3'
 
    queryStringParameters = event["queryStringParameters"]
    metricName = queryStringParameters['metricName'] if 'metricName' in queryStringParameters else 'NumberOfObjects'
    bucketName = queryStringParameters['bucketName']
    dimensions = []
    # See https://docs.aws.amazon.com/AmazonS3/latest/userguide/metrics-dimensions.html#s3-cloudwatch-dimensions for all the available metrics
    if metricName in ['NumberOfObjects']:
        dimensions = [{"Name": "BucketName", "Value": bucketName }, {"Name": "StorageType", "Value": "AllStorageTypes" }]
    else:
        dimensions = [{"Name": "BucketName", "Value": bucketName }, {"Name": "StorageType", "Value": "StandardStorage" }]


    return get_cloudwatch_metrics(namespace, metricName, dimensions, event)
