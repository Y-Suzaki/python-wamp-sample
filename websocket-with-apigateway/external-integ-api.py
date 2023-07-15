import json
import sys
import os
import boto3


api_gateway = boto3.client(
    service_name='apigatewaymanagementapi',
    endpoint_url=os.getenv('API_URL')
)


def get_connection_id() -> list[str]:
    table = os.getenv('DYNAMODB_TABLE')
    dynamodb = boto3.client('dynamodb')

    options = {
        'TableName': table
    }
    response = dynamodb.scan(**options)

    return response['Items'] if 'Items' in response else []


def post_to_connection(connection_id: str):
    message = json.dumps({
        "action": "sendmsg",
        "message": "lambda_websocket_client"
    })

    print("connectionId: " + connection_id)
    print("message: " + str(message))

    try:
        response = api_gateway.post_to_connection(
            Data=message, ConnectionId=connection_id)
    except Exception as e:
        print(e)
        sys.exit(1)

    print(response)


def lambda_handler(event, context):
    connection_ids = get_connection_id()

    for connection_id in connection_ids:
        post_to_connection(connection_id['id']['S'])

    return {"statusCode": 200}


if __name__ == "__main__":
    lambda_handler({}, {})
