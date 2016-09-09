import json
import threading
import time
from soundGenerator import SoundGenerator
from twitter import TwitterInterface, TweetConsumer

# Seconds
REMOVE_CITIZEN_TIME = 5 * 60


class TwitterListener(TweetConsumer):
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
		
	# FIXME: Should be 'consumeTweet' now
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
		print("Is citizen: " + str(self.tw.getCitizen(uid)))
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
		

class TwitterConnection(object):
	def __init__(self, queue, followListPolitician, polBack, birdBack, twitter: TwitterInterface):
		self.birdBack = birdBack
		self.polBack = polBack
		self.citizens = dict()
		self.poList = followListPolitician
		self.queue = queue
		self.lock = threading.RLock()
		self.twitter = twitter
		self.listener = TwitterListener(self.queue, self, self.polBack, self.birdBack)
		self.twitter.register(followListPolitician, self.listener)

	def getCitizen(self, cid):
		with self.lock:
			res = self.citizens.get(str(cid))
		return res

	def addCitizen(self, twittername, birdid):
		tid = self.twitter.resolve_name(twittername)
		if tid is None:
			print("no such user: " + twittername)
			return
		# Need the lock due to __removeCitizen
		if self.getCitizen(tid) is not None or self.isPoli(tid):
			print("already added: " + twittername)
			return

		entry = dict()
		entry["userId"] = str(tid)
		entry["birdId"] = birdid
		entry["startingTime"] = time.time()
		
		print("add citizen " + str(entry))

		with self.lock:
			if str(tid) in self.citizens:
				print("Don't call addCitizen from multiple threads, dude!")
			else:
				self.citizens[str(tid)] = entry
				self.twitter.register([twittername], self.listener)
				threading.Timer(REMOVE_CITIZEN_TIME,
								self.__remove_citizen, tid).start()

	def __remove_citizen(self, tid):
		with self.lock:
			del self.citizens[str(tid)]

	def isPoli(self, uid):
		tmp = False
		with self.lock:
			tmp = str(uid) in self.poList
		return tmp
