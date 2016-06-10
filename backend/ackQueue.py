import threading
import json
import pika

class AckQueue(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self, daemon=True)
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
		self.channel = self.connection.channel()


		

	def run(self):
		self.channel.queue_declare(queue='ack', durable=True)
                      
	def sendMessage(self, msg):
		print("Sended following in ack queue " + str(msg))
		self.channel.basic_publish(exchange='', routing_key='ack', body=json.dumps(msg))
