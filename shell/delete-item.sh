#!/usr/bin/env bash

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source "${script_dir}/base.sh"

read -r -d '' json <<EOF
{
  "Key": {
    "vehicle": {
      "S": "Honda Fit"
    },
    "odometer": {
      "N": "25528"
    }
  },
  "TableName": "mileage"
}
EOF

ddb delete-item --cli-input-json "${json}"
