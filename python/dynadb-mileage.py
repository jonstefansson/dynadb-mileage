import sys
import csv
import time
import datetime
import boto3
import fileinput
from botocore.exceptions import ClientError


class Fillup:

    def __init__(self, vehicle='Fit', odometer=None, date=None, gallons=None, trip=None, mpg=None, note=None):
        self.vehicle = vehicle
        self.odometer = int(odometer)
        self.date = build_date(date)
        self.gallons = float(gallons)
        self.mpg = mpg or round(float(trip) / float(gallons), 2)
        self.note = note

    def __repr__(self):
        return 'Fillup(vehicle=\'{0.vehicle:s}\', odometer={0.odometer}, date=\'{0.date:s}\', gallons={0.gallons:.3f}, mpg={0.mpg:.2f}, note={0.note})'\
            .format(self)

    def as_item(self):
        item = {
            'vehicle': {'S': 'Honda Fit'},
            'odometer': {'N': str(self.odometer)},
            'date': {'S': self.date},
            'gallons': {'N': str(self.gallons)},
            'mpg': {'N': str(self.mpg)}
        }
        if self.note:
            item['note'] = {'S': self.note}
        return item


def build_date(date_string):
    month, day, year = date_string.rsplit('/')
    return datetime.date(int(year), int(month), int(day)).isoformat()

def dynamodb():
    return boto3.client('dynamodb')

def dict_to_item(dict):
    return {
        'vehicle': {'S': 'Honda Fit'},
        'odometer': {'N': dict['Odometer']},
        'date': {'S': build_date(dict['Date'])},
        'gallons': {'N': dict['Gallons']},
        'mpg': {'N': dict['MPG']}
    }

def load():
    """Reads CSV fillup data from stdin
    Usage: python dynadb-mileage.py load < input.csv"""
    with fileinput.input() as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            fillup = Fillup(odometer=row['Odometer'], date=row['Date'], gallons=row['Gallons'], trip=row['Trip'], note=row['Note'])
            insert(fillup)
            time.sleep(1)

def insert(fillup):
    try:
        response = dynamodb().put_item(
            TableName='mileage',
            Item=fillup.as_item(),
            ConditionExpression='attribute_not_exists(odometer)'
        )
        print(response)
    except ClientError as e:
        print(e)

def load_csv():
    with open('/Users/jon/Downloads/Mileage - Fit.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = {
                'vehicle': {'S': 'Honda Fit'},
                'odometer': {'N': row['Odometer']},
                'date': {'S': build_date(row['Date'])},
                'gallons': {'N': row['Gallons']},
                'mpg': {'N': row['MPG']}
            }
            if len(row['Note']) > 0:
                item['note'] = {'S': row['Note']}
            try:
                response = dynamodb().put_item(
                    TableName='mileage',
                    Item=item,
                    ConditionExpression='attribute_not_exists(odometer)'
                )
                print(response)
            except ClientError as e:
                print(e)
            time.sleep(1)

def query(odometer):
    """Queries database for all records with an odometer reading greater than odometer"""
    try:
        result = dynamodb().query(
            TableName='mileage',
            ExpressionAttributeNames = {'#dt': 'date'},
            ExpressionAttributeValues={
                                        ':v1': {
                                                 'S': 'Honda Fit'
                                         },
                                         ':v2': {
                                                 'N': odometer
                                         }
                                     },
            KeyConditionExpression='vehicle = :v1 AND odometer > :v2',
            ProjectionExpression='#dt,odometer,mpg,note',
            ConsistentRead=False,
            Limit=25,
            ScanIndexForward=False
        )
        for item in result['Items']:
            print(
                '{0} | {1} | {2:.2f} | {3}'.format(
                    item['odometer']['N'],
                    item['date']['S'],
                    float(item['mpg']['N']),
                    item.get('note', {'S': ''}).get('S')
                )
            )
    except ClientError as e:
        print(e)


if __file__ == sys.argv[0]:
    command = sys.argv.pop(1)
    if command == 'load':
        load()
    elif command == 'query':
        query(sys.argv[1])