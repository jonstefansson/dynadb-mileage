import boto3
import json
import logging
import sys


logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_client():
    return boto3.client('dynamodb')


client = get_client()


def query(event):
    query_params = event.get('queryStringParameters', {})
    odometer = query_params.get('odometer', '30000') if query_params is not None else '30000'
    result = client.query(
        TableName='mileage',
        ExpressionAttributeNames = {'#dt': 'date'},
        ExpressionAttributeValues={':v1': {'S': 'Honda Fit'}, ':v2': {'N': odometer}},
        KeyConditionExpression='vehicle = :v1 AND odometer > :v2',
        ProjectionExpression='#dt,odometer,mpg,note',
        ConsistentRead=False,
        Limit=25,
        ScanIndexForward=False
    )
    return [
        dict(
            odometer=item.get('odometer', {}).get('N'),
            date=item.get('date', {}).get('S'),
            mpg=item.get('mpg', {}).get('N'),
            note=item.get('note', {}).get('S', '')
        )
        for item in result.get('Items')
    ]


def lambda_handler(event, context):
    logger.info('event: %r', event)
    results = query(event)
    proxy_response = dict(
        statusCode=200,
        body=json.dumps(results),
        isBase64Encoded=False
    )
    return proxy_response

