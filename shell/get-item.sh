#!/usr/bin/env bash
# Preventing referencing undefined variables
set -o nounset
# Do not ignore failing commands
set -o errexit

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source "${script_dir}/base.sh"

ddb get-item --cli-input-json '
{
    "TableName": "mileage", 
    "Key": {
        "vehicle": {
            "S": "Honda Fit"
        },
        "odometer": {
          "N": "278"
        }
    }, 
    "ConsistentRead": false, 
    "ReturnConsumedCapacity": "TOTAL"
}
'
