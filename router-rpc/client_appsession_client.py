import os
from datetime import datetime

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class ClientSession(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")
        # sub = yield self.subscribe(self.on_event, 'com.myapp.hello')
        yield self.register(self.utcnow, 'my.com.date.client')
        print('Call my.com.date.server')
        yield self.call('my.com.date.server')
        # now = yield self.call('my.com.date.server')
        # print(f'my.com.date.client. {now}')
        # print("Subscribed to com.myapp.hello with {}".format(sub.id))

    def on_event(self, i):
        print("Got event: {}".format(i))

    def utcnow(self):
        now = datetime.utcnow()
        print('********************************')
        print("Call RPC. my.com.date.client")
        print('********************************')
        return now.strftime("%Y-%m-%dT%H:%M:%SZ")

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
