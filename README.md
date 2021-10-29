# Deploy to AWS Lambda (First time)
sam build --profile csx --region us-east-1

sam deploy --stack-name sam-lambda \
	--profile csx \
	--region us-east-1 \
	--guided

# Deploy to AWS Lambda (Subsequent times)
sam build --profile csx --region us-east-1

sam deploy

# Destroy infrastructure
sam delete --no-prompts --profile csx

# Endpoints
## Query Params
The following query parameters can be sent with all api calls or just use the defaults as per the table
Query Parameter | Required| Default Value| Description
------------ | ------------- | ------------- | -------------
metricName | Yes| | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Metric
period | No | 60 | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#CloudWatchPeriods
stat | No| Sum |https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic
label | No| label | Descriptive lable for the data being returned (e.g. CPUUtilization, peak of ${MAX} was at ${MAX_TIME})
scanBy | No| TimestampDescending| How to order the mertrics. Valid values are TimestampDescending or TimestampAscending
previousDays | No| 0 | Number of days to retrieve metrics for - 0 is current day, 1 is current day and previous day etc.


**/fetch-airflow-metrics**

**Type:** GET

**Sample Endpoint:** https://5j1q4mnrt8.execute-api.us-east-1.amazonaws.com/Prod/fetch-airflow-metrics?metricName=OrphanedTasksAdopted

**/fetch-sagemaker-metrics**

**Type:** GET

**Sample Endpoint:** https://5j1q4mnrt8.execute-api.us-east-1.amazonaws.com/Prod/fetch-sagemaker-metrics?metricName=Invocations

**/fetch-custom-sagemaker-metrics**

**Type:** GET

**Sample Endpoint:** https://5j1q4mnrt8.execute-api.us-east-1.amazonaws.com/Prod/fetch-custom-sagemaker-metrics?metricName=MemoryUtilization

**/fetch-s3-metrics**

**Type:** GET

**Sample Endpoint:** https://5j1q4mnrt8.execute-api.us-east-1.amazonaws.com/Prod/fetch-s3-metrics?metricName=NumberOfObjects&bucketName=my-bucket

## Query Params
Query Parameter | Required| Description
------------ | ------------- | ------------- 
bucketName | Yes | Bucket to get metrics for

**/fetch-api-gateway-metrics**

**Type:** GET

**Sample Endpoint:** https://5j1q4mnrt8.execute-api.us-east-1.amazonaws.com/Prod/fetch-api-gateway-metrics?metricName=4XXError


## OLD Queries
**/fetch-cloudwatch-metrics**

**Type:** POST

**Sample Endpoint:** https://5j1q4mnrt8.execute-api.us-east-1.amazonaws.com/Prod/fetch-cloudwatch-metrics?namespace=AmazonMWAA&metricName=SchedulerHeartbeat&period=3660&stat=Sum&label=TempLabel&scanBy=TimestampDescending&previousDays=0

## Query Params
Query Parameter | Required| Default Value| Description
------------ | ------------- | ------------- | -------------
namespace | Yes | |https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Namespace
metricName | Yes| | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Metric
period | No | 60 | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#CloudWatchPeriods
stat | No| Sum |https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic
label | No| label | Descriptive lable for the data being returned (e.g. CPUUtilization, peak of ${MAX} was at ${MAX_TIME})
scanBy | No| TimestampDescending| How to order the mertrics. Valid values are TimestampDescending or TimestampAscending
previousDays | No| 0 | Number of days to retrieve metrics for - 0 is current day, 1 is current day and previous day etc.

See https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_GetMetricData.html#API_GetMetricData_Examples for examples
## Sample Body  
```
[
  {
    "Name": "Function",
    "Value": "Scheduler"
  },
  {
    "Name": "Environment",
    "Value": "csx-nonprod-dataops"
  }
]
```


