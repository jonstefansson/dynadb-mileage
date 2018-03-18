# API Gateway and Lambda Function 

* [Build an API Gateway API with Lambda Proxy Integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html)
* [AWS API Gateway: Solving Missing Authentication Tokens](http://www.awslessons.com/2017/aws-api-gateway-missing-authentication-token/)
* [AWS API Gateway: Adding API keys to your HTTP requets](http://www.awslessons.com/2017/aws-api-gateway-adding-apikey-requests/)
* [Solving AWS Lambda and API Gateway Internal Server Errors](http://www.awslessons.com/2017/lambda-api-gateway-internal-server-error/)
* [Using Lambda Functions with API Gateway](http://www.awslessons.com/2017/setting-up-lambda-with-api-gateway/)

This is what the Lambda function event looks like for a GET request.

```json
{
  "resource": "/{proxy+}",
  "path": "/mileage",
  "httpMethod": "GET",
  "headers": {
    "accept": "*/*",
    "Host": "775f4i6l7i.execute-api.us-east-1.amazonaws.com",
    "User-Agent": "curl/7.54.0",
    "X-Amzn-Trace-Id": "Root=1-5aa609e5-3d8939d07f61771862900ce0",
    "x-api-key": "eSd3RRbOckaeu2bJn6HD79Lt6CUGnjf93mzgwnpx",
    "X-Forwarded-For": "71.83.153.49",
    "X-Forwarded-Port": "443",
    "X-Forwarded-Proto": "https"
  },
  "queryStringParameters": {
    "odometer": "31600"
  },
  "pathParameters": {
    "proxy": "mileage"
  },
  "stageVariables": null,
  "requestContext": {
    "requestTime": "12/Mar/2018:05:02:29 +0000",
    "path": "/prod/mileage",
    "accountId": "557516168365",
    "protocol": "HTTP/1.1",
    "resourceId": "9n0x1a",
    "stage": "prod",
    "requestTimeEpoch": 1520830949985,
    "requestId": "90e0ad99-25b2-11e8-a8a7-23697d752322",
    "identity": {
      "cognitoIdentityPoolId": null,
      "cognitoIdentityId": null,
      "apiKey": "eSd3RRbOckaeu2bJn6HD79Lt6CUGnjf93mzgwnpx",
      "cognitoAuthenticationType": null,
      "userArn": null,
      "apiKeyId": "n2xnxga958",
      "userAgent": "curl/7.54.0",
      "accountId": null,
      "caller": null,
      "sourceIp": "71.83.153.49",
      "accessKey": null,
      "cognitoAuthenticationProvider": null,
      "user": null
    },
    "resourcePath": "/{proxy+}",
    "httpMethod": "GET",
    "apiId": "775f4i6l7i"
  },
  "body": null,
  "isBase64Encoded": false
}
```

Here's a POST request event:

```json
{
  "resource": "/{proxy+}",
  "path": "/mileage",
  "httpMethod": "POST",
  "headers": {
    "accept": "application/json",
    "content-type": "application/json; charset=utf-8",
    "Host": "775f4i6l7i.execute-api.us-east-1.amazonaws.com",
    "User-Agent": "curl/7.54.0",
    "X-Amzn-Trace-Id": "Root=1-5aad8a2b-206694ed42af9a6699bb4a0b",
    "x-api-key": "eSd3RRbOckaeu2bJn6HD79Lt6CUGnjf93mzgwnpx",
    "X-Forwarded-For": "71.83.153.49",
    "X-Forwarded-Port": "443",
    "X-Forwarded-Proto": "https"
  },
  "queryStringParameters": null,
  "pathParameters": {
    "proxy": "mileage"
  },
  "stageVariables": null,
  "requestContext": {
    "requestTime": "17/Mar/2018:21:35:39 +0000",
    "path": "/prod/mileage",
    "accountId": "557516168365",
    "protocol": "HTTP/1.1",
    "resourceId": "9n0x1a",
    "stage": "prod",
    "requestTimeEpoch": 1521322539248,
    "requestId": "22e95fb4-2a2b-11e8-a0ae-db08620ce1a1",
    "identity": {
      "cognitoIdentityPoolId": null,
      "cognitoIdentityId": null,
      "apiKey": "eSd3RRbOckaeu2bJn6HD79Lt6CUGnjf93mzgwnpx",
      "cognitoAuthenticationType": null,
      "userArn": null,
      "apiKeyId": "n2xnxga958",
      "userAgent": "curl/7.54.0",
      "accountId": null,
      "caller": null,
      "sourceIp": "71.83.153.49",
      "accessKey": null,
      "cognitoAuthenticationProvider": null,
      "user": null
    },
    "resourcePath": "/{proxy+}",
    "httpMethod": "POST",
    "apiId": "775f4i6l7i"
  },
  "body": "{ \"Fillups\": [ { \"Odometer\": 32462, \"Date\": \"03/09/2018\", \"Gallons\": 7.808, \"Trip\": 266.9, \"Note\": \"\" } ]}",
  "isBase64Encoded": false
}
```