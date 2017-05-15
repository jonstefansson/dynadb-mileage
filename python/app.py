import csv
import time
import datetime
import boto3
from botocore.exceptions import ClientError

def convertDate(datestr):
    month, day, year = datestr.rsplit('/')
    return datetime.date(int(year), int(month), int(day)).isoformat()

client = boto3.client('dynamodb')

with open('/Users/jon/Downloads/Mileage - Fit.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        item = {
            'vehicle': {'S': 'Honda Fit'},
            'odometer': {'N': row['Odometer']},
            'date': {'S': convertDate(row['Date'])},
            'gallons': {'N': row['Gallons']},
            'mpg': {'N': row['MPG']}
        }
        if len(row['Note']) > 0:
            item['note'] = {'S': row['Note']}
        try:
            response = client.put_item(
                TableName='mileage',
                Item=item,
                ConditionExpression='attribute_not_exists(odometer)'
            )
            print(response)
        except ClientError as e:
            print(e)
        time.sleep(1)
