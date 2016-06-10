import settings
import logging as log
import sys
from twitterAccountModule import TempTwitterStruct


class WikiTwitMatcher:
	def __init__(self, polList, twitList):
		# read alias file
		# match it
		self.aliases = {}
		self.polList = polList
		self.twitList = twitList
		f = open(settings.aliasFile)
		
		lineCount = 1
		for line in f:
			print(line)
			if line.startswith("#") or line.startswith("\n"):
				lineCount += 1
				continue
				
			try:
				arr = line.split(":=")
			except Exception:
				log.error("Did not found proper syntax in line " + str(lineCount))
				sys.exit(1)
				
			if len(arr) != 2:
				log.error("Did not found proper syntax in line " + str(lineCount))
				sys.exit(1)
				
			#print(arr)
			first = arr[0].strip()
			
			
		
			#sec = arr[1].split(",")
			
			#if sec is None:
			sec = arr[1].strip()
			self.aliases[sec.strip()] = first.strip()
				
	
			#for alias in sec:
			#	self.aliases[alias.strip()] = first.strip()
				
			
				
		
	def getAliases(self):
			return self.aliases
				
				
	def process(self):
			for (alias, realName) in self.aliases.items():
				for tempTwitter in self.twitList:
					if alias == tempTwitter.getName():
						
						tempTwitter.setName(realName)
						
			found = False
						
			for politian in self.polList:
				
				toRemove = None
				for twitTemp in self.twitList:
					if politian.getName() == twitTemp.getName():
						toRemove = twitTemp
						politian.setTwitterData(twitTemp.getScreenName(), twitTemp.getId())
						
				if toRemove is not None:
					self.twitList.remove(toRemove)
					
			if len(self.twitList) > 0:
				log.info("After matching, there are " + str(len(self.twitList))  + " left. \n Please match them by hand or specify aliases accordingly")
				for twitTemp in self.twitList:
					print(twitTemp.getName() + " " + twitTemp.getScreenName() + " "+  str(twitTemp.getId()))
				
						
						
					
	def getPolitians(self):
		return self.polList			
		
