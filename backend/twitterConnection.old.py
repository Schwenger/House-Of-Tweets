from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import threading
import time
from soundGenerator import SoundGenerator


class TwitterListener(StreamListener):
	def __init__(self, sendingQueue, tw, politicianBackend, birdBack):
		super().__init__()
		self.birdsList = birdBack.getAllBirds()
		self.sendingQueue = sendingQueue
		self.tw = tw
		self.pb = politicianBackend
		
	def createTestTweet(self, name, twittername, byPoli, content, time, tid, partycolor, image, soundc, soundp, retweeted, refresh, pdur, cdur):
		d = {}
		d["name"] = name
		d["twitterName"] = twittername
		d["byPoli"] = byPoli
		d["content"] = content
		d["time"] = time
		d["id"] = tid
		d["partycolor"] = partycolor
		d["image"] = image
		d["soundc"] = [soundc, cdur]
		
		if soundp is None:
			d["soundp"] = None
		else:
			d["soundp"] = [soundp, pdur]
			
		d["retweet"] = retweeted
		d["refresh"] = refresh
		
		return d

	# This is functionally equivalent to:
	# 'retweeted_status' in tweet
	def isRetweet(self, tweet):
		re = True
		try:
			bla = tweet["retweeted_status"]

		except Exception as e:
			re = False
			print(e)
	
		return re
		
	def getHashtags(self, tweet):
		hashTags = []
		try:
			hh = tweet["entities"]["hashtags"]
			
			for s in hh:
				tmp = s["text"].lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss").lower()
				hashTags.append(tmp)
		except Exception as e:
			print("Exception + "  + str(e))
			
		print(hashTags)
		
		if len(hashTags) > 0:
			print("house of tweets is in hashTags " + str("houseoftweet" in hashTags))
			if "houseoftweets" in hashTags:		
				print("found houseoftweets hashtag")
				return hashTags
		else:
			print("did not found the hashtag")
			return None
		

	def on_data(self, status):
		print("Receives Tweet\n" + status)
		status = json.loads(status)
		
		send = True
		try:
			status["delete"]
			send = False
		except Exception:
			send = True
			
		if not send:
			return
		
		uid = status["user"]["id"]
		print("Is poli" + str(self.tw.isPoli(uid)) + " " + str(uid) + " ")
		print("Is citizen: " + str(self.tw.isCitizen(uid)))
		if  not self.tw.isPoli(uid) and not self.tw.isCitizen(uid):
			return 
			
		hashTags = self.getHashtags(status)
		
		
		
		# TODO parse hashtag "houseoftweets"
		
		isPolitician = self.tw.isPoli(status["user"]["id"])
		
		tweetId = status["id"]
		content = status["text"]
		isRetweet = self.isRetweet(status)
		print("isReteweet? " + str(isRetweet))
		politician = None
		
		if isPolitician:
			politician = self.pb.getPolitician(status["user"]["id"])
		else:
			politician = self.tw.getCitizen(status["user"]["id"])
			
		refresh = None
	
		if hashTags is not None and isPolitician:
			# Do Something here
			
			for s in content.split(" "):
				tmp = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss").lower().strip()
				print("TMPPPPPPPPPPP is " + tmp)
				print(self.birdsList)
				if tmp in self.birdsList:
					print("new bird is " + tmp)
					
					pid = self.pb.setPoliticiansBird(status["user"]["id"], tmp)
					refresh = { "politicianId" :pid , "birdId" : tmp}

		cBird = None
		if isPolitician:
			cBird = politician["citizen_bird"]
		else:
			cBird = politician["birdId"]
		
		pBird = None
		
		if isPolitician:
			pBird = politician["self_bird"]

		color = None
		party = None 
		if isPolitician:
			party = politician["party"].lower().strip()
		
		if party is None:
			color = "#ffffff"
		elif party.startswith("c"):
			color = "#000000"
		elif party.startswith("s"):
			color = "#ff0000"
		elif party.startswith("g"):
			color = "#00cc00"
		elif party.startswith("d"):
			color = "#c82864"
		else:
			color = "#ffffff"

		gen = SoundGenerator()
		(pPath, cPath, pdur, cdur) = gen.makeSounds(tweetId, content, isRetweet, cBird, pBird)

		tweet = self.createTestTweet(status["user"]["name"], status["user"]["screen_name"], self.tw.isPoli(status["user"]["id"]), content, status["timestamp_ms"] ,tweetId, color, status["user"]["profile_image_url_https"], cPath, pPath, isRetweet, refresh, pdur, cdur)

		self.sendingQueue.addTweet(tweet)
		

class TwitterConnection:
	def __init__(self, queue, followListPolitician, polBack, birdBack):
		self.birdBack = birdBack
		self.polBack = polBack
		self.citizens = []
		self.poList = followListPolitician
		self.queue = queue
		self.lock = threading.RLock()
		
		l = TwitterListener(self.queue, self, self.polBack, self.birdBack)
		self.auth = CENSORED
		self.auth.set_access_token(CENSORED)
		self.api = tweepy.API(self.auth)
		self.stream = Stream(self.auth, l)
		self.stream.filter(follow = followListPolitician, async=True)
		self.timer = threading.Timer(5*60, self.cleanCitizens)
		self.timer.start()

	def getTwitterId(self, name):
		return str(self.api.get_user(name).id)
		
	def getCitizen(self, cid):
		res = None
		with self.lock:
			for c in self.citizens:
				if c["userId"] == str(cid):
					res = c
					break
		return res

	def addCitizen(self, twittername, birdid):
		entry = {}
		try:
			tid = self.api.get_user(twittername).id
		except Exception as e:
			print(e)
			return
		entry["userId"] = str(tid)
		entry["birdId"] = birdid
		entry["startingTime"] = time.time()
		
		print("added user " + str(entry))
		
		with self.lock:
			# FIXME What was this condition, and what did it do?
			# if entry not in self.citizens:
			self.citizens.append(entry)
			self.rebuildStream()
			
	def isPoli(self, uid):
		tmp = False
		with self.lock:
			tmp = str(uid) in self.poList
		return tmp
		
	def isCitizen(self, uid):
		tmp = False
		with self.lock:
			for e in self.citizens:
				if e["userId"] == str(uid):
					tmp = True
					break
		return tmp
			
	def cleanCitizens(self):
		delta = 5*60
		now = time.time()
		toDelete = []
		re = False
		with self.lock:
			for i in range(0, len(self.citizens)):
				e = self.citizens[i]
				print(str(e["startingTime"] + delta) + "<" + str(now))
				if e["startingTime"] + delta < now:
					toDelete.append(i)
			print("delete " + str(len(toDelete)))  
			if len(toDelete) > 0:
				re = True
				for i in toDelete:
					del self.citizens[i]
				
		if re == True:		
			self.rebuildStream()
		self.timer = threading.Timer(5*60, self.cleanCitizens)
		self.timer.start()

	def rebuildStream(self):
		self.stream.disconnect()
		
		with self.lock:
			fo= list(self.poList)
			
			for e in self.citizens:
				fo.append(e["userId"])
				
			self.stream = Stream(self.auth, TwitterListener(self.queue, self, self.polBack, self.birdBack))
			self.stream.filter(follow = fo, async=True)
