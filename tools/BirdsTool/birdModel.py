import json

class Bird:
	
	def __init__(self, bid, de_name, fr_name, en_name, latin_name, de_cv, fr_cv, en_cv):
		self.bid = bid
		self.de_name = de_name
		self.fr_name = fr_name
		self.en_name = en_name
		self.latin_name = latin_name
		self.de_cv = de_cv
		self.fr_cv = fr_cv
		self.en_cv = en_cv
		
		
class BirdModel:
	def __init__(self):
		#self.pathToFile = pathToFile
		self.birds = {}
		
	
		
	def addBird(self, bid, de_name, fr_name, en_name, latin_name, de_cv, fr_cv, en_cv):
		self.birds.append(Bird(bid, de_name, fr_name, en_name, latin_name, de_cv, fr_cv, en_cv))
		

		
	def getAllBirds(self):
		return self.birds
	
	def parseBlock(self, i, wFile, keyWords):
		print("here")
		count = 1
		for j in range(i+1, len(wFile)):
					nLine = wFile[j].strip()
					
					if nLine == "end":
						#print(keyWords)
						inBlock = False
						break
				
					arr = nLine.split(":=")
					try:
						keyWords[arr[0].strip()] = arr[1].strip()
					except Exception as e:
						print("This should not happen. At line " + str(i+1+count))
				 
					count += 1
					print(count)
					continue 
		return (count+1, keyWords) 
		
	def parseBirds(self):
		try :
			f = open("birds.txt") 
		except Exception:
			log.error("no file found")
			
		
		result = {}
		inBlock = False

		keyWords = {"bid": None, "de_name":None, "fr_name":None, "en_name":None, "latin_name": None, "de_cv":None, "fr_cv":None, "en_cv":None}
		wFile = []
		for line in f:
			wFile.append(line)
	
		#print(wFile)
		
		inBlock = False
	
		i = 0	
		while i < len(wFile):
			
			line = wFile[i].replace("\ufeff","")
			#print(i)
			if line == "\n" or line.startswith("#"):
				#print("here")
				i += 1
				continue
			
			line = line.strip()
			
			
			if line == "end" and not inBlock:
				log.error("Found end inside a block at line " + str(i))
				sys.exit(1)
		
			print(repr(line))
			print(line == "begin")
			if line == "begin" and not inBlock:
				print("here")
				(c, res) = self.parseBlock(i, wFile, dict(keyWords))
				i += c
				
				name = res["bid"]
				del res["bid"]
				self.birds[name] = res
				inBlock = False
			
			else:
				if line == "begin" and inBlock:
					log.error("Found begin inside a block at line " + str(i))
					sys.exit(1)
				
		
				
				
		
#test
b = BirdModel()
b.parseBirds()
pl = b.getAllBirds()

w = open("modelBirds.coffee", 'w')
w.write("model.birds = " )

json.dump(pl, w, indent=2)
		
