class TwitterAccountData:
	"""
	Encapsulates an id of a Twitter user and his/her screen name. Can be NONE 
	"""
	def __init__(self, twitterId, twitterScreenName):
		self.twitterId = twitterId
		self.twitterScreenName = twitterScreenName
		
	def getTwitterId(self):
		return self.twitterId
		
	def getTwitterScreenName(self):
		return self.twitterScreenName
		
	def debug(self):
		return self.twitterId + " " + self.twitterScreenName
	
	
class WikipediaData:
	def __init__(self, wikiLink, wikiDescription):
		self.wikiLink = wikiLink
		self.wikiDescription = wikiDescription
		
	def getWikipediaLink(self):
		return "de.wikipedia.org"+self.wikiLink
		
	def getWikipediaDescription(self):
		return self.wikiDescription
		
	def debug(self):
		return self.wikiLink + " " + self.wikiDescription


class Politian:
	def __init__(self, polId, name, pathToImage, wikipediaData, twitterAccountData):
		self.polId = polId
		self.name = name
		self.pathToImage = pathToImage
		self.wikipediaData = wikipediaData
		self.twitterAccountData = twitterAccountData 
		
	def getId(self):
		return self.polId
	
	def getName(self):
		return self.name
		
	def getPathToImage(self):
		return self.pathToImage
		
	def getWikipediaData(self):
		return self.wikipediaData
		
	def getTwitterAccountData(self):
		return self.twitterAccountData
		
	def debug(self):
		wiki = self.wikipediaData
		if wiki is None:
			wiki = "none none"
		else:
			wiki = self.wikipediaData.debug()
		twit = self.twitterAccountData
		
		if twit is None:
			twit = "none none"
		else:
			twit = self.twitterAccountData.debug()
		return self.polId + " " + self.name + " " + self.pathToImage + " " + wiki + " " + twit
		


class PolitianData:
	def __init__(self, pathToCSV):
		self.pathToCSV = pathToCSV
		self.data = []
		
	def getAllPolitians(self):
		""" 
		Returns the list of all politian objects
		"""
		return self.data
		
	def parse(self):
		"""
		call to add content to the list
		"""
		polFile = open(self.pathToCSV, 'r')
		
		for line in polFile:
			splitted = line.split("\t")
			if len(splitted) != 7:
				raise AssertionError("Wrong input format: length of Line = " + len(splitted))
			#id name pathToFile wikiLink wikiDesck twitternumber twittername
			polId      = splitted[0]
			name       = splitted[1]
			pathToFile = splitted[2]
			wikiLink   = splitted[3]
			wikiDesc   = splitted[4]
			twitNum    = splitted[5]
			twitName   = splitted[6]
			
			twitterData = None
			
			if wikiDesc == "none":
				wikiDesc = "Keine Beschreibung vorhanden"
				
			if twitNum != "none" and twitName != "none":
				twitterData = TwitterAccountData(twitNum, twitName)
				
			tmp = Politian(polId, name, pathToFile, WikipediaData(wikiLink, wikiDesc), twitterData)
			self.data.append(tmp)
				


