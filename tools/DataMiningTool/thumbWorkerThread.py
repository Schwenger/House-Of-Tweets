import threading
import queue
from PIL import Image
import logging as log

class ThumbWorkerThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self, daemon=True)
		self.q = queue.Queue()
		
		
		
	def addJob(self, fileName):
		self.q.put(fileName)
		
	def run(self):
		log.info("Thumbnail creator thread started")
		while True:
			job = self.q.get()
			
			if job is None:
				break
			
			try:	
				im = Image.open(job)
				im.thumbnail((75,75))
				im.save("t" + job, "JPEG")
			
			except Exception as e:
				log.error("An error occured while creating a thumb: " + e)
			
			log.info("Thumbnail creator thread stopped")
			
		
