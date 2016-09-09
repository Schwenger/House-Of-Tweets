import json


class BirdBackend:
	def __init__(self):
		self.bJson = json.load(open("birds.json"))
		self.bList = []
		
		for b in self.bJson:
			b = b.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss").lower().strip()
			self.bList.append(b)
			
	def getAllBirds(self):
		return self.bList
