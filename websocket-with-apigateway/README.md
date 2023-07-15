## 概要
APIGateway（WebSocket）にSubscribeしたクライアントに対し、外部APIからPublishしたい。

## 方法
1. boto3 生成時、Endpointを指定する。
```python
client = boto3.client(
    service_name='apigatewaymanagementapi',
    endpoint_url=os.getenv('API_URL')
)
```
2. post_to_connection で通知。
```python
try:
    response = client.post_to_connection(
        Data=message, ConnectionId=connection_id)
except Exception as e:
    print(e)
    sys.exit(1)
```
