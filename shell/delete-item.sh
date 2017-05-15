#!/usr/bin/env bash

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source "${script_dir}/base.sh"

read -r -d '' json <<EOF
{
  "Key": {
    "id": {
      "S": "4863E27A-EC53-4EBD-B427-4CF6B2006DFF"
    },
    "odometer": {
      "N": "23566"
    }
  },
  "TableName": "mileage"
}
EOF

ddb delete-item --cli-input-json "${json}"
