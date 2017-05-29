#!/usr/bin/env bash
# Preventing referencing undefined variables
# set -o nounset
# Do not ignore failing commands
# set -o errexit

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source "${script_dir}/base.sh"

json=''
read -r -d '' json <<-EOF
{
  "ConditionExpression": "attribute_not_exists(odometer)",
  "Item": {
    "vehicle": {
      "S": "Honda Fit"
    },
    "odometer": {
      "N": "24687"
    },
    "date": {
      "S": "2017-05-22"
    },
    "gallons": {
      "N": "7.693"
    },
    "mpg": {
      "N": "35.75"
    }
  },
  "TableName": "mileage"
}
EOF
ddb put-item --cli-input-json "${json}"
