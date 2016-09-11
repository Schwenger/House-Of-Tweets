import pika
import json
import threading


class CitizenBirdQueueAdapter(threading.Thread):
	def __init__(self, politicianBackend):
		threading.Thread.__init__(self, daemon=True)
		self.politicianBackend = politicianBackend
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
		host='localhost'))

	def run(self):
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='citizenbirds', durable=True)
		self.channel.basic_consume(self.callback, queue="citizenbirds", no_ack=True)
		self.channel.start_consuming()

	def callback(self, ch, method, properties, body):
		body = json.loads(body.decode('utf-8'))
		print("set !!!!!!!!!!!!!!!!!!!!!!!" + str(body))
		self.politicianBackend.setBird(body["politicianid"], body["birdid"], actor='c')
