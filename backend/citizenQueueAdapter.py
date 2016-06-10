import pika
import json
import threading
class CitizenQueueAdapter(threading.Thread):
	def __init__(self, twitterConnection):
		threading.Thread.__init__(self, daemon=True)
		self.twitterConnection = twitterConnection
		#here
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
		
	
	def run(self):
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='citizenuser', durable=True)
		self.channel.basic_consume(self.callback, queue="citizenuser", no_ack=True)
		self.channel.start_consuming()
		
	def callback(self, ch, method, properties, body):
		body = json.loads(body.decode('utf-8'))
		#body = json.loads(str(body))
		#print(body)
		#body = json.loads(body)
		print(body)
		self.twitterConnection.addCitizen(body["twittername"], body["birdid"])
