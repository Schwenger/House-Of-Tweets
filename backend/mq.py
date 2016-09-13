import json
import pika
import threading


class SendQueueInterface(object):
    def post(self, _):
        raise NotImplementedError("Should have implemented this")


def connection():
    return pika.BlockingConnection(pika.ConnectionParameters('localhost'))


class RealQueue(SendQueueInterface):
    def __init__(self, name):
        self.connection = connection()
        self.channel = self.connection.channel()
        self.name = name
        self.channel.queue_declare(queue=name, durable=True)

    def post(self, message):
        print('Publishing on queue {name}: {data!r}'
              .format(name=self.name, data=message))
        if self.connection.is_closed:
            print("Whoops, connection is closed; reopen.")
            self.connection = connection()
            self.channel = self.connection.channel()
        try:
            self.channel.basic_publish(exchange='', routing_key=self.name,
                                       body=json.dumps(message))
        except Exception as e:
            print("Connection failed anyway?  Make sure RabbitMQ is running! (is_closed = {})".format(self.connection.is_closed))
            print(e.__repr__())
            print("Message dropped.")

    @staticmethod
    def new(name):
        return RealQueue(name)


class PrintQueue(SendQueueInterface):
    def __init__(self, name):
        self.name = name
        # Technically, reading (and asserting against) this property
        # is always a data race.  Practically, fuck you.
        self.msgs = []

    def post(self, message):
        print('Would send this to MQ {name}: {data!r}'
              .format(name=self.name, data=message))
        self.msgs.append(message)

    @staticmethod
    def new(name):
        return PrintQueue(name)

    def expect(self, msgs_expect):
        assert self.msgs == msgs_expect, (self.msgs, msgs_expect)
        self.msgs = []


BATCH_TIMEOUT = 5


class Batcher(SendQueueInterface):
    def __init__(self, queue: SendQueueInterface):
        self.tweets = []
        self.connection = queue
        self.timer = None
        self.lock = threading.RLock()

    def post(self, msg):
        with self.lock:
            self.tweets.append(msg)
            if self.timer is None:
                self.timer = \
                    threading.Timer(BATCH_TIMEOUT, self.__send)
                self.timer.start()

    def __send(self):
        with self.lock:
            toSend = self.tweets
            self.tweets = []
            self.timer = None
        self.connection.post(toSend)
