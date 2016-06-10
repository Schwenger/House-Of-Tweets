import settings
import sys
import logging as log
from politianDataModel import Politian

def parseBlock(i, wFile, keyWords):
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
					log.error("This should not happen. At line " + str(count))
				 
				count += 1
				continue 
	return (count+1, keyWords) 
	


def parseCustomPolitiansList(nextId):
	try :
		f = open(settings.customPolitianFile) 
	except Exception:
		log.error("no file found")
		return None
		
	result = []
	inBlock = False

	keyWords = {"name": None, "party":None, "gender":None, "imageOrig":None, "imageThum": None, "wikiLink":None, "wikiDesc":None, "twitId":None, "twitUserName":None}
	wFile = []
	for line in f:
		wFile.append(line)
	
	print(wFile)
		
	inBlock = False
	
	i = 0	
	while i < len(wFile):
		
		line = wFile[i]
		print(i)
		if line == "\n" or line.startswith("#"):
			#print("here")
			i += 1
			continue
			
		line = line.strip()
			
		if line == "end" and not inBlock:
			log.error("Found end inside a block at line " + str(i))
			sys.exit(1)
		
			
		if line == "begin" and not inBlock:
			(c, res) = parseBlock(i, wFile, dict(keyWords))
			i += c
			#polId, name, party, gender, imageOrig, imageThum, wikiLink, wikiDesc, twitId, twitUserName
			result.append(Politian(nextId, res["name"], res["party"], res["gender"], res["imageOrig"], res["imageThum"], res["wikiLink"], res["wikiDesc"], res["twitId"], res["twitUserName"]))
			nextId += 1
		else:
			if line == "begin" and inBlock:
				log.error("Found begin inside a block at line " + str(i))
				sys.exit(1)
				
		
				
				
		
		
	return result
