import boto3
import json
import datetime

stream_name = 'kfh-clickStream'     #name of a stream in Firehose
firehose_client = boto3.client('firehose', region_name='ap-southeast-1')

def lambda_handler(event, context):
    # Extract details from the API Gateway event
    ip = event['requestContext']['http']['sourceIp']
    method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path'].replace('/','\\\\')
    parameters = event['rawQueryString']    #optional
    timestamp = event['requestContext']['time']

    # Parse timestamp string to datetime object
    timestamp_dt = datetime.datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
    # Format datetime object to desired format (12Mar2020T19)
    formatted_timestamp = timestamp_dt.strftime("%d%b%YT%H")

    # Create the record
    record = {
        'ip': ip,
        'timestamp': formatted_timestamp,
        'method': method,
        'path': path,
        'params': parameters
    }

    # Sending data to Kinesis Firehose
    response = firehose_client.put_record(
        DeliveryStreamName=stream_name,
        Record={
            'Data': json.dumps(record)
        }
    )

    return {"statusCode":200, "body":"success"}
