import pika
import json


class SendQueueInterface(object):
    def post(self, _):
        raise NotImplementedError("Should have implemented this")


class RealQueue(SendQueueInterface):
    def __init__(self, name):
        self.connection = \
            pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.name = name
        self.channel.queue_declare(queue=name, durable=True)

    def post(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.name,
                                   body=json.dumps(message))

    @staticmethod
    def new(name):
        return RealQueue(name)


class PrintQueue(SendQueueInterface):
    def __init__(self, name):
        self.name = name

    def post(self, message):
        print('Would send this to MQ {name}: {data!r}'
              .format(name=self.name, data=message))

    @staticmethod
    def new(name):
        return PrintQueue(name)
