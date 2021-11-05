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

# CloudWatch Endpoints

**/list-cloudwatch-namespaces**

**Type:** GET

**Purposes:** Lists all the namespaces that exist within the cloudwatch metrics for the current aws region

**Sample Endpoint:** https://d5un4aacsl.execute-api.us-east-1.amazonaws.com/Prod/list-cloudwatch-namespaces

**/list-cloudwatch-metrics**

**Type:** GET

**Query Params:** 
namespace - retrieved from list-cloudwatch-namespaces call

**Purposes:** Get all available metrics for a namespace. This returns the metrics as well as a list of all the dimensions for that metric

**Sample Endpoint:** https://d5un4aacsl.execute-api.us-east-1.amazonaws.com/Prod/list-cloudwatch-metrics?namespace=AmazonMWAA

**/fetch-cloudwatch-metrics**

**Type:** POST

**Query Params:** 
namespace - retrieved from list-cloudwatch-namespaces call
metricName - retrieved from the list-cloudwatch-metrics call

**Body:**  The body is the dimension we want to retrieve. The list-cloudwatch-metrics call returns a list of dimensions for a metric and namespace combination. We need to pass in 1 of these metrics

**Sample Endpoint:** https://d5un4aacsl.execute-api.us-east-1.amazonaws.com/Prod/fetch-cloudwatch-metrics?namespace=AmazonMWAA&metricName=CriticalSectionBusy

**Sample Endpoint:** https://d5un4aacsl.execute-api.us-east-1.amazonaws.com/Prod/fetch-cloudwatch-metrics?namespace=AmazonMWAA&metricName=CriticalSectionBusy&period=60&stat=Sum&label=TempLabel&scanBy=TimestampDescending&previousDays=0 

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
## Query Params
The following query parameters can be sent with the fetch-cloudwatch-metrics api call or just use the defaults as per the table. 

*Note*: namespace and metricName are required query params

Query Parameter | Required| Default Value| Description
------------ | ------------- | ------------- | -------------
namespace | Yes| | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Namespace
metricName | Yes| | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Metric
period | No | 60 | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#CloudWatchPeriods
stat | No| Sum |https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Statistic
label | No| label | Descriptive lable for the data being returned (e.g. CPUUtilization, peak of ${MAX} was at ${MAX_TIME})
scanBy | No| TimestampDescending| How to order the metrics. Valid values are TimestampDescending or TimestampAscending
previousDays | No| 0 | Number of days to retrieve metrics for - 0 is current day, 1 is current day and previous day etc.

# Sagemaker Endpoints

**/sagemaker/list-training-jobs**

**Type:** GET

**Purposes:** Lists all the training jobs that existin in AWS for the current aws region

**Sample Endpoint:** https://d5un4aacsl.execute-api.us-east-1.amazonaws.com/Prod/sagemaker/list-training-jobs

**/sagemaker/describe-training-job**

**Type:** GET

**Query Params:** 
trainingJobName - the trainingJobName retrieved in the list training jobs call

**Purposes:** Get the details from a specific training job

**Sample Endpoint:** https://d5un4aacsl.execute-api.us-east-1.amazonaws.com/Prod/sagemaker/describe-training-job?trainingJobName=mxnet-training-2021-11-01-05-23-15-483
