import pika
import json
import mylog
import threading


# Listen for a new citizen-assigned bird for a politician.
class CitizenBirdQueueAdapter(threading.Thread):
	def __init__(self, politicianBackend):
		threading.Thread.__init__(self, daemon=True)
		self.politicianBackend = politicianBackend
		self.next = None
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
		host='localhost'))

	def run(self):
		mylog.with_exceptions(self._run, self._restart)

	def _run(self):
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='citizenbirds', durable=True)
		self.channel.basic_consume(self.callback, queue="citizenbirds", no_ack=True)
		self.channel.start_consuming()

	def _restart(self):
		mylog.error('Stacking a new thread.  Please restart soon!')
		self.next = CitizenBirdQueueAdapter(self.politicianBackend)
		self.next.start()

	def callback(self, ch, method, properties, body):
		body = json.loads(body.decode('utf-8'))
		mylog.info("set citizen bird: {}".format(body))
		self.politicianBackend.setBird(body["politicianid"], body["birdid"], actor='c')
