import json
from random import randint

class cv:
	def __init__(self,de,fr,en):
		self.de = de
		self.en = en
		self.fr = fr

	
class twittering:
	def __init__(self,twitterId,	twitterUserName):
		self.twitterId = twitterId
		self.twitterUserName = twitterUserName
	
	
class images:
	def __init__(self,pathToImage, pathToThumb):
		self.pathToImage = pathToImage
		self.pathToThumb = pathToThumb
	

class OutputModel:
	def __init__(self, id, name, party, twittering, self_bird, citizen_bird, cv, images):
		self.id = id
		self.name = name
		self.party = party
		self.twittering = twittering
		self.self_bird = self_bird
		self.citizen_bird = citizen_bird
		self.cv = cv
		self.images = images
		
		
	def getTw(self):
		return self.twitter
		
	def getCv(self):
		return self.cv
		
	def getIm(self):
		return self.images

		

class OutputWriter:
	def __init__(self,politianList):
		self.politianList = politianList
		self.birdList = ['amsel', 'ara', 'bachstelze', 'blaumeise', 'buchfink', 'buntspecht', 'dohle', 'eichelhaeher', 'elster', 'feldsperling', 'fitis', 'gartenbaumläufer', 'gartengrasmücke', 'gartenrotschwanz', 'gimpel', 'girlitz', 'goldammer', 'grauschnäpper', 'grünfink', 'hausrotschwanz', 'haussperling', 'heckenbraunelle', 'kiwi', 'klappergrasmücke', 'kleiber', 'kohlmeise', 'mauersegler', 'mehlschwalbe', 'mönchsgrasmücke', 'rabenkrähe', 'rauchschwalbe', 'ringeltaube', 'rotkehlchen', 'saatkrähe', 'schneeeule', 'schwanzmeise', 'singdrossel', 'star', 'stieglitz', 'tannenmeise', 'tukan', 'türkentaube', 'weisskopfseeadler', 'zaunkönig', 'zilpzalp']
		
	
		
		
	def generateOutput(self):
		erg = "["
		for i in range(0, len(self.politianList)):
			po = self.politianList[i]
			
			i = None
			t= None
			c = None
			
			if po.getImages() is not None:
				i = images(po.getImages().getPathToOriginalImage(), po.getImages().getPathToThumb())
				
				
			if 	po.getTwitterData() is not None:
				t = twittering(po.getTwitterData().getTwitterId(), po.getTwitterData().getTwitterScreenName())
				
			if po.getWikipediaData() is not None:
				de = po.getWikipediaData().getWikipediaDescription()
				# X est un/e politicien/ne allemand/e. Il/Elle est un membre de la partie XY.
				fr = None
				en = None
				if po.getGender() == "M":
					fr = po.getName() + " est un politicien allemand. Il est un membre de la partie " + po.getParty() + "."
					en = po.getName() + " is a German politian. He is a member of the " + po.getParty() + "."
				else:
					if po.getGender() == "F":
						fr = po.getName() + " est une politicienne allemande. Elle est une membre de la partie " + po.getParty() + "."
						en = po.getName() + " is a German politian. She is a member of the " + po.getParty() + "."
						
				c = cv(de,fr,en)
				
			
			out = OutputModel(po.getId(), po.getName(), po.getParty(), t, self.birdList[randint(0, len(self.birdList)-1)], self.birdList[randint(0, len(self.birdList)-1)], c, i)
			
			if out.__dict__["images"] is not None:
				out.__dict__["images"] = out.__dict__["images"].__dict__
				
			if out.__dict__["cv"] is not None:
				out.__dict__["cv"] = out.__dict__["cv"].__dict__
				
			if out.__dict__["twittering"] is not None:
				out.__dict__["twittering"] = out.__dict__["twittering"].__dict__
			
			
			if i == len(self.politianList):
				erg += json.dumps(out.__dict__) 
			else:
				erg += json.dumps(out.__dict__) + ", \n"
			
			
		erg += "]"
		print(erg)
		fii = open("pols.json", "w")
		fii.write(erg)
		fii.close
