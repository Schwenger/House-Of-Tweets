import urllib.request
from bs4 import BeautifulSoup
from politianDataModel import Politian
import logging as log
import math
from wikipediaWorkerThread import WikipediaWorkerThread
import re



class WikipediaParser():
	
	def __init__(self, baseUrl):
		self.baseUrl = baseUrl
		self.threads = []
		self.politianList = []
		
		
	def startProcessing(self):
		self.polList = self.parseWikiTable()
		
		self.threads.append(WikipediaWorkerThread(0, 648, self.politianList))
		#self.threads.append(WikipediaWorkerThread(130, 260, self.politianList))
		#self.threads.append(WikipediaWorkerThread(260, 390, self.politianList))
		#self.threads.append(WikipediaWorkerThread(390, 520, self.politianList))
		#self.threads.append(WikipediaWorkerThread(520, 648, self.politianList))
		
		for thread in self.threads:
			thread.start()
		
	def awaitCompletion(self):
		for thread in self.threads:
			thread.join()
			
		return self.politianList
		
	def dump(self):
		f = open("dump.txt", "w")
		for p in self.politianList:
			f.write(p.getName()+ "\n")
		
	def parseWikiTable(self):
		count = 0
		
		data = urllib.request.urlopen(self.baseUrl).read()
		bs = BeautifulSoup(data, 'html.parser')
		regex = re.compile(r"\(([^\)]+)\)", re.IGNORECASE)

		table = bs.find("table", { "class" : "prettytable" })
		for row in table.findAll("tr"):
			entries = row.findAll("td")
			if len(entries) == 7:
				print(str(count))
				name = entries[0].a["title"]
				#name = name.replace("(CDU)", "");
				#name = name.replace("(CSU)"	, "");
				#name = name.replace("(SPD)", "");
				#name = name.replace("(Politiker)", "");
				#name = name.replace("(Politikerin)", "");
				#name = name.replace("(MdB)", "")
				name = name.replace("\t", "");
				#name = name.replace("", "")
				name = re.sub(regex, "", name)
				name = name.strip()
				
				
				
				wikilink = entries[0].a["href"]
				party = entries[2].string.strip()
				#polId,     name,          party,   gender, imageOrig=None, imageThum=None, wikiLink=None, wikiDesc=None, twitId=None, twitUserName=None
				self.politianList.append(Politian(count, name, party, None, None, None, wikilink, None, None, None))
			
				count += 1
	
		log.info("Found " + str(count) + " Politians")
		
