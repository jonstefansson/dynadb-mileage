#!/usr/bin/env bash

source .env

curl \
--silent \
--request POST \
--header "x-api-key: ${API_KEY}" \
--header "Accept: application/json" \
--header "Content-Type: application/json; charset=utf-8" \
--data @- \
"https://775f4i6l7i.execute-api.us-east-1.amazonaws.com/prod/mileage" \
<<EOF | jq '.'
{
    "Fillups": [
        {
            "Odometer": 32462,
            "Date": "03/09/2018",
            "Gallons": 7.808,
            "Trip": 266.9
        }
    ]
}
EOF
