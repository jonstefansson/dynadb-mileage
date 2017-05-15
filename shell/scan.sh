#!/usr/bin/env bash

script_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source "${script_dir}/base.sh"

ddb scan --cli-input-json '
{
   "ConsistentRead": true,
   "Limit": 10,
   "TableName": "mileage"
}
'
