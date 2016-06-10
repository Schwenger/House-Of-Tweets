import threading
import urllib.request
from bs4 import BeautifulSoup
from politianDataModel import Politian
import logging as log
from PIL import Image
from PIL import ImageFile
import settings
import wikipedia
import sys
import os
class WikipediaWorkerThread(threading.Thread):
	def __init__(self, start, end, model):
		threading.Thread.__init__(self, daemon=True)
		self.startPos = start
		self.endPos   = end
		self.model = model
		
		
	def getSummaryOfPolitian(self, bs):
		
		tmpBs = bs
		# mw-content-text
		t = (tmpBs.find('div',id="bodyContent").p.text)
		u = (tmpBs.find('div',id="mw-content-text").p.text)
		
		if t is None and u is None:
			print(bs)
			sys.exit(1)
			
		if t is not None:
			return t
			
		if u is not None:
			return u
		"""
		arr = url.split("/")
		wikipedia.set_lang("de")
		return wikipedia.summary(arr[len(arr)-1])
		"""
	
	def downloadFirstImage(self,fileName, bs):
		#bs = BeautifulSoup(data, 'html.parser')
		#imageTags = bs.findAll("image")
		imageTags = bs.find("div", { "class" : "thumbinner" })
	
		if imageTags is None:
			return None
	
		print(len(imageTags))
		link = None
		if (len(imageTags) > 0):
			for image in imageTags.findAll("a"):
				print(image["href"])
			
				try:
					if (".j" in image["href"].lower() or ".p" in image["href"].lower()) and not "thumb"in image["href"].lower():
						link = image["href"]
						break
				except Exception:
					continue			
			
		if link is not None:		
			data = urllib.request.urlopen("http://de.wikipedia.org" + link).read()
			bs = BeautifulSoup(data, 'html.parser')
			imageFrs = bs.find("div", { "class" : "fullImageLink" })
		else:
			return None
		
		for image in imageFrs.findAll("a"):
			print(image["href"])
			
			try:
				if (".j" in image["href"].lower() or ".p" in image["href"].lower()) and not "thumb"in image["href"].lower():
					link = image["href"]
					break
			except Exception:
				continue		
				
		print("http:" + link)	
		try:
			urllib.request.urlretrieve("http:" + link, "out/"+ fileName)
		except Exception as e:
			print("Encountered " +str(e))
			sys.exit(1)
		return fileName		
	
		

	def getGender(self,bs):
		# mw-normal-catlinks
		table = bs.find("div", { "class" : "mw-normal-catlinks" })
		erg = None
		for row in table.findAll("ul"):
			entries = row.findAll("li")
		
			for e in entries:
				if "Mann" in e.a["title"]:
					erg = ("M")
					break
			
				if "Frau" in e.a["title"]:
					erg = ("F")
					break
		return erg
		
		
	def createThumb(self, fileName):

		ImageFile.LOAD_TRUNCATED_IMAGES = True
		try:	
			im = Image.open("out/" + fileName)
			im.thumbnail(settings.thumbSize)
			im.save("out/" + "t" + fileName, "JPEG")
			
		except Exception as e:
			log.error("An error occured while creating a thumb: " + str(e))
			sys.exit(1)
		
		
		
	def run(self):
		log.info("Starting Working Thread")
		for i in range(self.startPos, self.endPos):
			# get i-th politian
			log.info("processing no. " + str(i))
			pol = self.model[i]
			url = pol.getWikipediaData().getWikipediaLink()
			data = urllib.request.urlopen(url).read()
			bs = BeautifulSoup(data, "html.parser")
			
			summary = self.getSummaryOfPolitian(bs)
			gender  = self.getGender(bs)
						
			image   = self.downloadFirstImage(str(pol.getId())+".jpg", bs)
			
			if image is not None:
				# create thumb
				self.createThumb(image)
				pol.setPathsToImages(image, "t" + image)
				
			pol.setWikipediaDescription(summary)
			pol.setGender(gender)
		
		log.info("Stopping Working Thread")
			
			
			
	
