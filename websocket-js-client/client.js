import WebSocket from 'ws';

console.log('Start.')

const options = {
  headers: {
    Authorization: 'test1234'
  }
}

const ws = new WebSocket(
  'wss://n41tp3e8i3.execute-api.ap-northeast-1.amazonaws.com/production',
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