#!/usr/bin/env bash

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source "${script_dir}/base.sh"

ddb query --cli-input-json '
{
  "KeyConditionExpression": "vehicle = :v1 AND odometer > :v2",
  "ExpressionAttributeValues": {
    ":v1": {
      "S": "Honda Fit"
    },
    ":v2": {
      "N": "25000"
    }
  },
  "ExpressionAttributeNames": {"#dt": "date"},
  "ProjectionExpression": "#dt,vehicle,odometer,mpg,note",
  "ConsistentRead": false,
  "Limit": 25,
  "ScanIndexForward": false,
  "TableName": "mileage"
}
' | jq '.'
# jq '.Items[0]'