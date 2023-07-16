## 概要
NodejsのWebsocketライブラリを利用して、AWS API GatewayのWebsocketに接続する。  
認証はIAMを設定する。

## 認証
1. API Gatewayの`$connect`の認証にIAMを設定する。
2. Nodejsの環境変数に、AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEYを設定する。
    * サンプルのため、アクセスキーを直接設定している。
    * 本来であれば、LambdaなどのIAM Roleから一時Credentialを取得するのが良い。
3. Websocket Subscribe時に、sigv4署名を生成、ヘッダに設定する。
    ```js
    const signatureV4 = new SignatureV4({
      service: 'execute-api',
      region: 'ap-northeast-1',
      credentials: {
        accessKeyId: env.AWS_ACCESS_KEY_ID,
        secretAccessKey: env.AWS_SECRET_ACCESS_KEY,
      },
      sha256: Sha256,
    });
    ```
4. HTTPリクエスト内容に従って署名を生成する。
    ```js
    const request = new HttpRequest({
      protocol: 'wss',
      hostname: 'n41tp3e8i3.execute-api.ap-northeast-1.amazonaws.com',
      path: '/production',
      method: 'GET',
      headers: {
        host: 'n41tp3e8i3.execute-api.ap-northeast-1.amazonaws.com'
      }
    })
   
    const signedRequest = await signatureV4.sign(request);
    const options = {
      headers: {
        ...signedRequest.headers
      }
    }
    ```
5. Websocket生成（Connect）時、リクエストヘッダに署名を渡す。
    ```js
    const ws = new WebSocket(
      'wss://n41tp3e8i3.execute-api.ap-northeast-1.amazonaws.com/production',
      undefined,
      options
    );
    ```
