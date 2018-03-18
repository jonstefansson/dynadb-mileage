import boto3
import json
import logging
import sys
from collections import namedtuple
from botocore.exceptions import ClientError
from datetime import date


logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
Route = namedtuple('Route', ['path', 'httpMethod'])
Response = namedtuple('Response', ['statusCode', 'body'])


def get_client():
    return boto3.client('dynamodb')


client = get_client()


def route(event):
    """
    Routes the event to the appropriate function for handling the request.

    :param event:
    :return: a Response namedtuple with statusCode and body attributes
    """

    def query():

        def item_to_dict(item):
            return dict(
                Odometer=item.get('odometer', {}).get('N'),
                Date=item.get('date', {}).get('S'),
                MPG=item.get('mpg', {}).get('N'),
                Note=item.get('note', {}).get('S', '')
            )

        query_params = event.get('queryStringParameters', {})
        odometer = query_params.get('odometer', '30000') if query_params is not None else '30000'
        query_results = client.query(
            TableName='mileage',
            ExpressionAttributeNames={'#dt': 'date'},
            ExpressionAttributeValues={':v1': {'S': 'Honda Fit'}, ':v2': {'N': odometer}},
            KeyConditionExpression='vehicle = :v1 AND odometer > :v2',
            ProjectionExpression='#dt,odometer,mpg,note',
            ConsistentRead=False,
            Limit=25,
            ScanIndexForward=False
        )
        body = [item_to_dict(item) for item in query_results.get('Items')]
        return Response(200, body)

    def insert_fillups():

        def insert(fillup):

            def as_item():

                def build_date():
                    date_string = fillup.get('Date')
                    month, day, year = [int(s) for s in date_string.rsplit('/')]
                    return date(year, month, day).isoformat()

                def calculate_mpg():
                    trip = fillup.get('Trip')
                    gallons = fillup.get('Gallons')
                    return round(float(trip) / float(gallons), 2)

                item = {
                    'vehicle': {'S': 'Honda Fit'},
                    'odometer': {'N': str(fillup.get('Odometer'))},
                    'date': {'S': build_date()},
                    'gallons': {'N': str(fillup.get('Gallons'))},
                    'mpg': {'N': str(calculate_mpg())}
                }
                if 'Note' in fillup:
                    item['note'] = {'S': fillup.get('Note')}
                return item

            try:
                client.put_item(
                    TableName='mileage',
                    Item=as_item(),
                    ConditionExpression='attribute_not_exists(odometer)'
                )
                logger.info('Fillup inserted: %r', fillup)
                return fillup
            except ClientError as ex:
                logger.exception(ex)

        post_data = json.loads(event.get('body'))
        inserted_fillups = [insert(fillup) for fillup in post_data.get('Fillups', [])]
        return Response(200, dict(inserted=inserted_fillups))

    def not_found():
        return Response(404, dict(error=f"No resource for {request_route}"))

    try:
        request_route = Route(event.get('path'), event.get('httpMethod'))

        if request_route == Route('/mileage', 'GET'):
            return query()
        elif request_route == Route('/mileage', 'POST'):
            return insert_fillups()
        else:
            return not_found()
    except Exception as e:
        logger.exception(e)


def lambda_handler(event, context):
    logger.info('event: %r', event)
    response = route(event)
    proxy_response = dict(
        statusCode=response.statusCode,
        body=json.dumps(response.body),
        isBase64Encoded=False
    )
    return proxy_response
