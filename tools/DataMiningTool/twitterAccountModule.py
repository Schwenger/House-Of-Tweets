import threading
import tweepy
from tweepy.auth import OAuthHandler
import settings
#import logging as log
import sys
from urllib.parse import urlparse

class TempTwitterStruct:
	# member.name.strip(),member.screen_name.strip() , member.id
	def __init__(self, name, screenName, mId):
		self.name = name
		self.screenName = screenName
		self.mId = mId
		
	def getName(self):
		return self.name
		
	def getScreenName(self):
		return self.screenName
		
	def getId(self):
		return self.mId
		
	def setName(self, neu):
		self.name = neu
	


class TwitterUserListExtractor(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self, daemon=True)
		
		#log.getLogger("tweepy").setLevel(log.ERROR)
		#log.getLogger("tweepy.auth").setLevel(log.ERROR)
		#log.getLogger("OAuthHandler").setLevel(log.ERROR)

		
		settings.twitterSettingsFilePath
		self.twitterLists = []
		f = open(settings.twitterSettingsFilePath, "r")
		
		self.consumerKey = None
		self.consumerSecret = None
		self.accesToken = None
		self.accessTokenSecret = None
		
		self.result = None
		self.blackList = []
		
		lineCount = 1
		for line in f:
			if line.startswith("#") or line.startswith("\n"):
				lineCount += 1
				continue
			
			try:
				arr = line.split(":=")
			except Exception:
				#log.error("Encountered sytax error at line " + str(lineCount) + "!\n See syntax definition in file")
				sys.exit(1)
				
			if len(arr) < 2:
				print("Error at line " + str(lineCount) +"!")
			else:
				# consumerKey, consumerSecret, accesToken, accessTokenSecret 
				first = arr[0].strip()

				if first == "blackList":
					try:
						lists = arr[1].split(",")
					except Exception:
						self.blackList.append(arr[1].strip())
						
					for e in lists:
						self.blackList.append(e.strip())
						
					lineCount += 1
					continue

				if first == "lists":
					try:
						lists = arr[1].split(",")
					except Exception:
						self.twitterlists.append(self.parseTwitterListLinks(arr[1].strip()))
						
					for e in lists:
						parsed = self.parseTwitterListLinks(e.strip())
						self.twitterLists.append(parsed)
						
					lineCount += 1
					continue
				
				if first == "consumerKey":
					if len(arr) != 2:
						print("Given Consumerkey is not a single word. Line " + lineCount)
					else:
						self.consumerKey = arr[1].strip()
						lineCount += 1	
						continue
						
				if first == "consumerSecret":
					if len(arr) != 2:
						print("Given ConsumerSecret is not a single word. Line " + lineCount)
					else:
						self.consumerSecret = arr[1].strip()
						lineCount += 1	
						continue
					
				if first == "accesToken":
					if len(arr) != 2:
						print("Given accessToken is not a single word. Line " + lineCount)
					else:
						self.accesToken = arr[1].strip()
						lineCount += 1
						continue
					
				if first == "accessTokenSecret":
					if len(arr) != 2:
						print("Given accessTokenSecret is not a single word. Line " + lineCount)
					else:
						self.accessTokenSecret = arr[1].strip()
						lineCount += 1
						continue
				
				#log.error("Syntax error encountered at line " + str(lineCount) +"! Unknown keyword found") 
				sys.exit(1)
				
		if self.consumerKey is None:
			print("You forgot to specify the consumerKey!")
			sys.exit(1)
			
		if self.consumerSecret is None:
			print("You forgot to specify the consumerKey!")
			sys.exit(1)
			
		if self.accesToken is None:
			print("You forgot to specify the consumerKey!")
			sys.exit(1)
			
		if self.accessTokenSecret is None:
			print("You forgot to specify the consumerKey!")
			sys.exit(1)
				
	
	def parseTwitterListLinks(self, rawLink):
		
		try:
				tmp = urlparse(rawLink)
		except Exception as e :
			#log.error("Twitter list link is not a valid url: " + str(e))
			sys.exit(1)
		print(tmp)
		if tmp.netloc != "twitter.com":
			#log.error("Twitter list link is not a twitter valid url. Instead, the parser found " + tmp.netloc)
			sys.exit(1)
			
		path = tmp.path
		path = path[1:]
		arr = path.split("/")
		
		if len(arr) != 3:
			#log.error("Something is wrong with the provided link")
			sys.exit(1)
		else:
			return (arr[0], arr[2])
		
			
			
		
	def run(self):
		auth = OAuthHandler(self.consumerKey, self.consumerSecret);
		auth.set_access_token(self.accesToken, self.accessTokenSecret)
		api = tweepy.API(auth)
		
		self.result = []
		
		print(self.blackList)
		
		for (user, name) in self.twitterLists:
			for member in tweepy.Cursor(api.list_members, user, name).items():
				if (member.screen_name.strip() not in self.blackList):
					self.result.append( TempTwitterStruct(member.name.strip(),member.screen_name.strip() , member.id))
				else:
					print("Found blacklisted " + member.screen_name.strip())
			
		
		
		
		
	def awaitTermination(self):
		self.join()
		return self.result
		
