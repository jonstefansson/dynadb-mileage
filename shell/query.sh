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
      "N": "300"
    }
  },
  "ConsistentRead": false,
  "Limit": 1,
  "ScanIndexForward": false,
  "TableName": "mileage"
}
'
