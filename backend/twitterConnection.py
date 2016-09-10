import re
import threading
import time
from soundGenerator import generate_sound
from twitter import TwitterInterface, TweetConsumer
import mq

# Seconds
REMOVE_CITIZEN_TIME = 5 * 60

COMMAND_HASHTAGS = {'houseoftweets', 'house_of_tweets', 'hot', 'house-of-tweets'}


def party_to_color(party: str):
	party = party.lower()
	"""
Currently, these are *all* parties in our dataset:
CDU
CSU
Demokraten
DIE LINKE
GR\u00dcNE
Gr\u00fcn
Parti socialiste
SPD
	"""

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

	return color


def contains_command(hashtags):
	for h in hashtags:
		if h.lower() in COMMAND_HASHTAGS:
			return True
	return False


def find_bird(content, birdBack):
	content = content.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
	words = set(re.sub("[^\wäöüß]", " ",  content).split())
	for candidate in words:
		bird = birdBack.bJson.get(candidate)
		if bird is not None:
			return [candidate, bird]
	return None


class TwitterListener(TweetConsumer):
	def __init__(self, sendingQueue: mq.SendQueueInterface, tw, politicianBackend, birdBack):
		super().__init__()
		self.birdBack = birdBack
		self.sendingQueue = sendingQueue
		self.tw = tw
		self.pb = politicianBackend
		self.prev_msg_id = 42 - 1

	def consumeTweet(self, tweet):
		self.prev_msg_id += 1
		print("Received tweet # {}".format(tweet))

		# Boring stuff
		msg = dict()
		msg['byPoli'] = self.tw.isPoli(tweet['uid'])
		msg['content'] = tweet['content']
		msg['hashtags'] = tweet['hashtags']
		msg['id'] = self.prev_msg_id
		msg['image'] = tweet['profile_img']
		msg['name'] = tweet['userscreen']
		msg['retweet'] = tweet['retweet']
		msg['time'] = tweet['time']
		msg['twitterName'] = tweet['username']

		# Resolve politician/citizen specifics
		if msg['byPoli']:
			birds = self.handle_poli(tweet, msg)
		else:
			citizen = self.tw.getCitizen(tweet['uid'])
			if citizen is None:
				print("Outdated tweet by no-longer citizen {}".format(tweet['uid']))
				birds = None
			else:
				birds = self.handle_citizen(citizen, msg)

		# Make a sound
		if birds is None:
			print("=> drop tweet, DONE")
			return
		msg['sound'] = generate_sound(tweet['content'], tweet['retweet'], birds)

		# Send it
		self.sendingQueue.post(msg)
		print("Done with this tweet, DONE.")

	# For consistency.
	# noinspection PyMethodMayBeStatic
	def handle_citizen(self, citizen, msg):
		msg['partycolor'] = '#257E9C'  # some random, dark-ish blue
		# Don't define msg['refresh']
		return [citizen['birdId'], None]

	def handle_poli(self, tweet, msg):
		poli = self.pb.getPolitician(tweet['uid'])
		if poli is None:
			print("No poli for tracked poli-uid {} found".format(tweet['uid']))
			return None

		msg['partycolor'] = party_to_color(poli['party'])

		# Check for any updates
		if contains_command(tweet['hashtags']):
			pid = self.pb.tid2pid(poli['id'])
			bird = find_bird(tweet['content'], self.birdBack)
			if bird is None or pid is None:
				print('I saw that command, but bird={bird!r}, pid={pid!r} content={ct}'
						.format(ct=tweet['content'], bird=bird, pid=pid))
			else:
				print('politician "{}" ({}) gets new bird {}'
						.format(tweet['screenname'], poli['id'], bird))
				msg['refresh'] = dict()
				msg['refresh']['politicianId'] = pid
				msg['refresh']['birdId'] = bird
				self.pb.setPoliticiansBird(tweet['uid'], bird)

		# In case of 'refresh', poli already contains the update:
		return [poli['citizen_bird'], poli['self_bird']]


class TwitterConnection(object):
	def __init__(self, queue: mq.SendQueueInterface, followListPolitician,
				 polBack, birdBack, twitter: TwitterInterface):
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

	def addCitizen(self, twittername, birdid, tid=None):
		if tid is None:
			tid = self.twitter.resolve_name(twittername)
		if tid is None:
			print("citizen user ignored, invalid name: " + twittername)
			return
		birdid = birdid.lower()
		if birdid not in self.birdBack.bJson:
			print("citizen user ignored, invalid bird: " + birdid)
			return
		# Need the lock due to __removeCitizen
		if self.getCitizen(tid) is not None or self.isPoli(tid):
			print("already added: " + twittername)
			return

		entry = dict()
		entry["userId"] = str(tid)
		entry["birdId"] = birdid
		entry["party"] = 'neutral'
		entry["startingTime"] = time.time()
		
		print("add citizen " + str(entry))

		with self.lock:
			if str(tid) in self.citizens:
				print("Don't call addCitizen from multiple threads, dude!")
			else:
				self.citizens[str(tid)] = entry
				self.twitter.register([str(tid)], self.listener)
				timer = threading.Timer(REMOVE_CITIZEN_TIME,
										self._remove_citizen, tid)
				# Don't prevent shutting down
				timer.daemon = True
				timer.start()

	def _remove_citizen(self, tid):
		with self.lock:
			print("Removing citizen {}".format(tid))
			try:
				del self.citizens[str(tid)]
			except KeyError:
				pass
			print("Remaining citizens: {}".format(self.citizens.keys()))

	def isPoli(self, uid):
		with self.lock:
			return str(uid) in self.poList
