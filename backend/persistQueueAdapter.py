import pika
import json
import threading
from random import randint
import os
import hashlib
from ackQueue import AckQueue

class PersistQueueAdapter(threading.Thread):
	def __init__(self, politicianBackend, twi):
		threading.Thread.__init__(self, daemon=True)
		self.ackQueue = AckQueue()
		self.ackQueue.start()
		self.politicianBackend = politicianBackend
		self.birdList = ['amsel', 'ara', 'bachstelze', 'blaumeise', 'buchfink', 'buntspecht', 'dohle', 'eichelhaeher', 'elster', 'feldsperling', 'fitis', 'gartenbaumlaeufer', 'gartengrasmuecke', 'gartenrotschwanz', 'gimpel', 'girlitz', 'goldammer', 'grauschnaepper', 'gruenfink', 'hausrotschwanz', 'haussperling', 'heckenbraunelle', 'kiwi', 'klappergrasmuecke', 'kleiber', 'kohlmeise', 'mauersegler', 'mehlschwalbe', 'moenchsgrasmuecke', 'rabenkraehe', 'rauchschwalbe', 'ringeltaube', 'rotkehlchen', 'saatkraehe', 'schneeeule', 'schwanzmeise', 'singdrossel', 'star', 'stieglitz', 'tannenmeise', 'tukan', 'tuerkentaube', 'weisskopfseeadler', 'zaunkoenig', 'zilpzalp']
		self.twi = twi
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
		
	
	def run(self):
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='persist', durable=True)
		self.channel.basic_consume(self.callback, queue="persist", no_ack=True)
		self.channel.start_consuming()
		
	def callback(self, ch, method, properties, body):
		body = json.loads(body.decode('utf-8'))
		print(body)
		# TODO besteht aus 2 objekten: keylogin : {username:, password}
		#{'values': [{'male': True, 'name': 'Name', 'party': 'Partei', 'id': 'namepartei', 'remove': False, 'cv': 'Beschreibung', 'twittername': 'tweet'}], 
		#'login': {'uname': 'uname', 'h': 'a1e66c01f0395bb7949575ae4649c7f7669b40c4898cc39b2423ed199bacd9cb'}}

		login = body["login"]
		username = login["uname"]
		passw 	= login["h"]
		
		if username != "admin" and hashlib.sha256(b"admin") != passw:
			print("wrong credentials")
			body["error"] = "Wrong credentials"
			self.ackQueue.sendMessage(body)
			return
		
		values = body["values"] 
		
		for v in values:
			if v["remove"]:
				ret = self.politicianBackend.delPolitician(v["id"])
				
				if ret is not True:
					body["error"] = "Could not delete politician."
					self.ackQueue.sendMessage(body)
					
				print("written")
				print("call compile")
				print(os.getcwd())
				os.chdir("..")
				print(os.getcwd())
				os.system("sh compile.sh")
				print("remove " + str(v["id"]))
			
			else :
		
				cv = {}
				cv["de"] = v["cv"]
		
				if v["male"] == True:
					cv["fr"] = v["name"] + " est un politicien allemand. Il est une membre de la partie " + v["party"] + "."
					cv["en"] =v["name"] + " is a German politician. He is a member of the " + v["party"] + "."
				else :
					cv["fr"] = v["name"] +" est une politicienne allemande. Elle est un membre de la partie " +  v["party"] + "."
					cv["en"] = v["name"] +" is a German politician. She is a member of the " +  v["party"] + "."
		
				twittering = None
				if v["twittername"] != "":
					twittering = {}
					twittering["twitterId"] = self.twi.getTwitterId(v["twittername"])
					twittering["twitterUserName"] = v["twittername"]
			

				images = None
			
				if v["imagelink"] == "":
					images = None
				else:
					images = v["imagelink"]
				
		
				#(self, pid, name, party, twittering, self_bird, citizen_bird, cv, images)
				print("add ")
				ret = self.politicianBackend.addPolitician(v["id"], v["name"], v["party"], twittering, self.birdList[randint(0, len(self.birdList)-1)], self.birdList[randint(0, len(self.birdList)-1)], cv, images) 
				
				
				if ret is not True:
					body["error"] = "Politician did already exist"
					self.ackQueue.sendMessage(body)
			
