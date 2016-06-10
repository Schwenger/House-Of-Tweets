import queue
import threading
import pika
import json

class SendingQueueForTweets:
	def __init__(self):
		self.q = queue.Queue()
		self.timer = None
		self.lock = threading.RLock()
		self.qlock = threading.RLock()
		
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='tweets', durable=True)
		
	
	def addTweet(self, tweet):
		with self.qlock:
			self.q.put(tweet)
		
		with self.lock:
			if self.timer is None:
				self.timer = threading.Timer(5, self.sendTweetsToFrontEnd)
				self.timer.start() 
				
	def sendTweetsToFrontEnd(self):
		toSend = []
		with self.qlock:
			while not self.q.empty():
				toSend.append(self.q.get_nowait())
					
		self.channel.basic_publish(exchange='', routing_key="tweets",body=json.dumps(toSend))
		self.timer = None
                     
                      
           
		
				
	
			
		
