import json
import mq
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

	def run(self):
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='citizenuser', durable=True)
		self.channel.basic_consume(self.callback, queue="citizenuser", no_ack=True)
		self.channel.start_consuming()
		
	def callback(self, ch, method, properties, body):
		body = json.loads(body.decode('utf-8'))
		print(body)
		user = body["twittername"]
		bird = body["birdid"]
		err = self.twitterConnection.addCitizen(user, bird)
		self.nackQueue.post({'twittername': user, "birdid": bird, "error": err})
