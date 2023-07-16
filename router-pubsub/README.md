# python-wamp-sample

## crossbarの初回起動
1. バージョン確認
```shell
crossbar version
```

2. 新規で作成する場合はinit
```shell
crossbar init
```

3. Router起動
```shell
crossbar start --cbdir=./.crossbar
```

## PubSubの実装
1. Subscribe
```python
import os
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class ClientSession(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        sub = yield self.subscribe(self.on_event, 'com.myapp.hello')
        print("Subscribed to com.myapp.hello with {}".format(sub.id))

    def on_event(self, i):
        print("Got event: {}".format(i))

    def onDisconnect(self):
        print("disconnected")
        if reactor.running:
            reactor.stop()


if __name__ == '__main__':
    url = os.environ.get('CBURL', 'ws://localhost:8080/ws')
    realm = os.environ.get('CBREALM', 'realm1')

    extra = dict(
        max_events=5,  # [A] pass in additional configuration
    )
    runner = ApplicationRunner(url=url, realm=realm, extra=extra)
    runner.run(ClientSession, auto_reconnect=True)
```

2. Publish単発
```python
import os
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

from twisted.internet import reactor


class ClientSession(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        counter = 0
        print('backend publishing com.myapp.hello', counter)
        self.publish('com.myapp.hello', "Hello World %d"%counter)
        yield sleep(1)

        # １回Publishしたらすぐ切断。
        self.disconnect()

    def onDisconnect(self):
        print("disconnected")
        if reactor.running:
            reactor.stop()


if __name__ == '__main__':
    url = os.environ.get('CBURL', 'ws://localhost:8080/ws')
    realm = os.environ.get('CBREALM', 'realm1')

    extra = {
        'foobar': 'A custom value'
    }

    runner = ApplicationRunner(url=url, realm=realm, extra=extra)
    runner.run(ClientSession, auto_reconnect=True, start_reactor=True)

    print("End publish session.")
```