import WebSocket from 'ws';
import {config} from 'dotenv'
import { Sha256 } from '@aws-crypto/sha256-universal';
import { HttpRequest } from '@aws-sdk/protocol-http';
import { SignatureV4 } from '@aws-sdk/signature-v4';


console.log('Start.')

// AWS Key情報を環境変数から読み込み
config()
const env = process.env
console.log(env)

// sigv4署名を生成し、ヘッダに設定
const signatureV4 = new SignatureV4({
  service: 'execute-api',
  region: 'ap-northeast-1',
  credentials: {
    accessKeyId: env.AWS_ACCESS_KEY_ID,
    secretAccessKey: env.AWS_SECRET_ACCESS_KEY,
  },
  sha256: Sha256,
});

const request = new HttpRequest({
  protocol: 'wss',
  hostname: 'ntsqtgfbp1.execute-api.ap-northeast-1.amazonaws.com',
  path: '/production',
  method: 'GET',
  headers: {
    host: 'ntsqtgfbp1.execute-api.ap-northeast-1.amazonaws.com'
  }
})

const signedRequest = await signatureV4.sign(request);
const options = {
  headers: {
    ...signedRequest.headers
  }
}

// Websocketの接続時、認証用の署名を設定する。
const ws = new WebSocket(
  'wss://ntsqtgfbp1.execute-api.ap-northeast-1.amazonaws.com/production',
  undefined,
  options
);

ws.on('error', (error) => {
  console.log(error)
});

ws.on('open', () => {
  console.log('Success to connect.')
  // ws.send('something');
});

ws.on('close', () => {
  console.log('Success to close.')
});


ws.on('message', function message(data) {
  console.log('received: %s', data);
});

console.log('End')