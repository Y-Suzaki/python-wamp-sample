import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    print(event)

    dbname = os.environ['CLIENT_CONNECTION_TABLE']
    table = dynamodb.Table(dbname)

    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps({"result": 0}, ensure_ascii=False)
    }
