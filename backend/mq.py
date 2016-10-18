import json
import mylog
import pika
import threading


WRITE_TWEETS = True


class SendQueueInterface(object):
    def post(self, _):
        raise NotImplementedError("Should have implemented this")


def connection():
    return pika.BlockingConnection(pika.ConnectionParameters('localhost'))


class RealQueue(SendQueueInterface):
    def __init__(self, name, log_file=None):
        self.connection = connection()
        self.channel = self.connection.channel()
        self.name = name
        self.channel.queue_declare(queue=name, durable=True)
        self.lock = threading.RLock()
        self.log_file = log_file
        # We never "close" a connection, so thankfully we don't need to ever stop the "heart":
        self._heartbeat()

    def maybe_log_message(self, msg):
        import os.path
        if self.log_file is None:
            return
        if not WRITE_TWEETS:
            return
        mylog.debug('Writing to {}: {}'.format(self.log_file, msg))
        old = []
        # Let's hope there are never two backend running simultaneously
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as fp:
                old = json.load(fp)
        old.append(msg)
        with open(self.log_file, 'w') as fp:
            json.dump(old, fp, sort_keys=True, indent=1)

    def post(self, message, isRetry=False):
        mylog.info('Publishing on queue {name}: {data!r}'
                   .format(name=self.name, data=message))
        with self.lock:
            if self.connection.is_closed:
                mylog.warning("Whoops, connection is closed; reopen.")
                self.connection = connection()
                self.channel = self.connection.channel()
            try:
                self.channel.basic_publish(exchange='', routing_key=self.name,
                                           body=json.dumps(message))
                self.maybe_log_message(message)
            except Exception as e:
                mylog.error("Connection failed anyway?  Make sure RabbitMQ is running! (is_closed = {})"
                            .format(self.connection.is_closed))
                mylog.error(e.__repr__())
                mylog.error(e.args)
                mylog.info("Message dropped.")
                if not isRetry:
                    self.post(message, True)

    def _heartbeat_wrap(self):
        mylog.with_exceptions(self._heartbeat)

    def _heartbeat(self):
        with self.lock:
            mylog.debug('pump: ' + self.name)
            self.connection.process_data_events()
            # RabbitMQ expects a heartbeat every 60 seconds, so send one every 30 seconds.
            timer = threading.Timer(30, self._heartbeat_wrap)
            timer.daemon = True
            timer.start()

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
        mylog.info('Would send this to MQ {name}: {data!r}'
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
                    threading.Timer(BATCH_TIMEOUT, self._send_wrap)
                self.timer.start()

    def _send_wrap(self):
        mylog.with_exceptions(self._send)

    def _send(self):
        with self.lock:
            toSend = self.tweets
            self.tweets = []
            self.timer = None
        self.connection.post(toSend)
