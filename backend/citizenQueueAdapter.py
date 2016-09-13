import pika
import json
import threading


# Listen for a user to enter his handle and favourite bird.
class CitizenQueueAdapter(threading.Thread):
	def __init__(self, twitterConnection):
		threading.Thread.__init__(self, daemon=True)
		self.twitterConnection = twitterConnection
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
		host='localhost'))

	def run(self):
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='citizenuser', durable=True)
		self.channel.basic_consume(self.callback, queue="citizenuser", no_ack=True)
		self.channel.start_consuming()
		
	def callback(self, ch, method, properties, body):
		body = json.loads(body.decode('utf-8'))
		print(body)
		self.twitterConnection.addCitizen(body["twittername"], body["birdid"])
