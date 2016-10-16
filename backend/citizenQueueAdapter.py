import json
import mq
import mylog
import pika
import threading


# Listen for a user to enter his handle and favourite bird.
class CitizenQueueAdapter(threading.Thread):
	def __init__(self, twitterConnection, nackQueue: mq.SendQueueInterface):
		threading.Thread.__init__(self, daemon=True)
		self.twitterConnection = twitterConnection
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
		host='localhost'))
		self.nackQueue = nackQueue
		self.next = None

	def run(self):
		mylog.with_exceptions(self._run, self._restart)

	def _run(self):
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='citizenuser', durable=True)
		self.channel.basic_consume(self.callback, queue="citizenuser", no_ack=True)
		self.channel.start_consuming()

	def _restart(self):
		mylog.error('Stacking a new thread.  Please restart soon!')
		self.next = CitizenQueueAdapter(self.twitterConnection, self.nackQueue)
		self.next.start()

	def callback(self, ch, method, properties, body):
		body = json.loads(body.decode('utf-8'))
		mylog.info("Add/set citizen user: {}".format(body))
		user = body["twittername"]
		bird = body["birdid"]
		err = self.twitterConnection.addCitizen(user, bird)
		response = {'twittername': user, "birdid": bird}
		if err is not None:
			response['error'] = err
		self.nackQueue.post(response)
