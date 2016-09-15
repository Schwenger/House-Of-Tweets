import json


class BirdBackend:
	def __init__(self):
		self.bJson = json.load(open("birds.json"))
		self.bList = []
		
		for b in self.bJson:
			b = b.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss").lower().strip()
			self.bList.append(b)

	# Always returns a string.  If everything goes wrong, it lies.
	def getName(self, bid):
		b = self.bJson.get(bid)
		if b is None:
			print('Tried to resolve invalid Bird-ID "{}",'
				  ' will go with "Goldammer" instead'.format(bid))
			return 'Goldammer'
		return b['de_name']


	def getAllBirds(self):
		return self.bList
