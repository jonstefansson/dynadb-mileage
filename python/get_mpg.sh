#!/usr/bin/env bash

source .env
odometer=${1:-31000}

curl \
--silent \
--request GET \
--header "x-api-key: ${API_KEY}" \
"https://775f4i6l7i.execute-api.us-east-1.amazonaws.com/prod/mileage?odometer=${odometer}" | jq '.'
