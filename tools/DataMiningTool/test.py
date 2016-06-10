import urllib.request
from bs4 import BeautifulSoup
from politianDataModel import Politian
from thumbWorkerThread import ThumbWorkerThread
import wikipedia
import threading
import math
import logging as log
from wikipediaWorkerThread import WikipediaWorkerThread
from wikipediaParser import WikipediaParser
from twitterAccountModule import TwitterUserListExtractor
import customPolitiansReader 
from wikiTwitMatcher import WikiTwitMatcher
from twitterAccountModule import TempTwitterStruct
from outputWriter import OutputWriter
from customPolitiansReader import *




def checkDependencies(self):
	try:
		import tweepy

	except Exception:
		log.error("Please install tweepy first")



log.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=log.DEBUG)

"""
url = "https://de.wikipedia.org/wiki/Liste_der_Mitglieder_des_Deutschen_Bundestages_(18._Wahlperiode)"
log.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=log.DEBUG)
wikiParser = WikipediaParser(url)
wikiParser.startProcessing()
end = wikiParser.awaitCompletion()
"""

"""
#parseWikiTable(url)

#getGender("https://de.wikipedia.org/wiki/Petra_Pau")
polList = parseWikiTable(url)


threads = []
numThreads = 5
cu = 0
part = math.floor(len(polList)/numThreads)

threads.append(WikipediaWorkerThread(0, 130, polList))
#threads.append(WikipediaWorkerThread(130, 260, polList))
#threads.append(WikipediaWorkerThread(260, 390, polList))
#threads.append(WikipediaWorkerThread(390, 520, polList))
#threads.append(WikipediaWorkerThread(520, 648, polList))
	
for thread in threads:
	thread.start()
	
for thread in threads:
	thread.join()
	
for pol in polList:
	print(pol.createOutput())
	
#getFirstImage("https://de.wikipedia.org/wiki/Jan_van_Aken_(Politiker)", "muuh.jpg")
	
	
# max size 75, 75

"""


	

url = "https://de.wikipedia.org/wiki/Liste_der_Mitglieder_des_Deutschen_Bundestages_(18._Wahlperiode)"
log.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=log.DEBUG)
wikiParser = WikipediaParser(url)
wikiParser.startProcessing()
polList = wikiParser.awaitCompletion()

tmp = parseCustomPolitiansList(len(polList))
polList.extend(tmp)
#wikiParser.dump()

		
	


print("done with parsing info")
print("start twitter stuff")
twitParser = TwitterUserListExtractor()
twitParser.start()
twitList = twitParser.awaitTermination()
print("end twitter stuff")
print("start mathing")
matcher = WikiTwitMatcher(polList, twitList)
matcher.process()
print("end matching")
OutputWriter(polList).generateOutput()






