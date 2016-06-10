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
		
	def createOutput(self):
		return str(self.twitterId) + " " + self.twitterScreenName
	
	
class WikipediaData:
	def __init__(self, wikiLink, wikiDescription=None):
		self.wikiLink = wikiLink
		self.wikiDescription = wikiDescription

	#def __init__(self, wikiLink):
	#	self.wikiLink = wikiLink
	#	self.wikiDescription = None

	def setWikipediaDescription(self, desc):
		self.wikiDescription = desc
		
	def getWikipediaLink(self):
		return "http://de.wikipedia.org"+self.wikiLink
		
	def getWikipediaDescription(self):
		return self.wikiDescription
		
	def createOutput(self):
		return self.wikiLink + " " + self.wikiDescription

class Images:
	def __init__(self, pathToOrginalImage, pathToThumb):
		self.pathToOrginalImage = pathToOrginalImage
		self.pathToThumb = pathToThumb
		
	def getPathToOriginalImage(self):
		return self.pathToOrginalImage
		
	def getPathToThumb(self):
		return self.pathToThumb
		
	def createOutput(self):
		return self.pathToOrginalImage + " " + self.pathToThumb
		
		

class Politian:
	"""
	def __init__(self, polId, name, party, gender, images, wikipediaData, twitterData):
		self.polId = polId
		self.name = name
		self.party = party
		self.gender = gender
		self.images = images
		self.wikipediaData = wikipediaData
		self.twitterData = twitterData
		
	def __init__(self, polId, name, party, wiki):
		self.polId = polId
		self.name = name
		self.party = party
		self.gender = None
		self.images = None
		self.wikipediaData = WikipediaData(wiki)
		self.twitterData =  None
	"""
	#"name": None, "party":None, "gender":None, "imageOrig":None, "imageThum": None, "wikiLink":None, "wikiDesc":None, "twitId":None, "twitUserName":None
	def __init__(self, polId, name, party, gender=None, imageOrig=None, imageThum=None, wikiLink=None, wikiDesc=None, twitId=None, twitUserName=None):
		self.polId = polId
		self.name = name
		self.party = party
		self.gender = gender
		
		if imageOrig is not None and imageThum is not None:
			self.images = Images(imageOrig, imageThum)
		else:
			self.images = None
		
		if wikiLink is not None and wikiDesc is not None:
			self.wikipediaData = WikipediaData(wikiLink, wikiDesc)
		else:
			if wikiLink is not None and wikiDesc is None:
				self.wikipediaData = WikipediaData(wikiLink)
			else:
				raise Exception("This should not happen")
				
		if twitId is not None and twitUserName is not None:
			self.twitterData = TwitterAccountData(twitId, twitUserName)
		else:
			self.twitterData = None
			
	def getName(self):
		return self.name
	
	def getParty(self):
		return self.party	
	
	def getId(self):
		return self.polId
		
	def setGender(self, gender):
		self.gender = gender
		
	def getGender(self):
		return self.gender
		
	def setPathsToImages(self, pathToOriginal, pathToThumb):
		if pathToOriginal is None or pathToThumb is None:
			raise Exception("None")
		self.images = Images(pathToOriginal, pathToThumb)
		
	def getImages(self):
		return self.images
		
	def setWikipediaLink(self, wikilink):
		if self.wikipediaData is None:
			self.wikipediaData = WikipediaData(wikilink)
			
	def setWikipediaDescription(self, desc):
		if self.wikipediaData is not None:
			self.wikipediaData.setWikipediaDescription(desc)
			
	def getWikipediaData(self):
		return self.wikipediaData
		
	def setTwitterData(self, userName, userId):
		self.twitterData = TwitterAccountData(userId, userName)
		
	def getTwitterData(self):
		return self.twitterData
		
	def createOutput(self):
		#polId, name, party, gender, images, wikipediaData, twitterData
		
		polId = str(self.polId)
		name = self.name
		party = self.party
		gender = self.gender
		images = self.images
		wiki = self.wikipediaData
		twit = self.twitterData
		
		if images is None:
			images = "none"
		else:
			images = self.images.createOutput()
			
		if wiki is None:
			raise Exception("Wiki cannot be None")
		else:
			if wiki.getWikipediaDescription() is not None:
				wiki = self.wikipediaData.createOutput()
			else:
				 wiki = self.wikipediaData.getWikipediaLink()
		if twit is None:
			twit = "none"
		else:
			twit = self.twitterData.createOutput()
		return polId + " " +name + " " + party +" " + gender+ " " + images + " " + wiki +" " +twit 
		




