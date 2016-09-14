import re
import threading
from soundGenerator import generate_sound
from twitter import TwitterInterface, TweetConsumer
import mq

# Seconds
REMOVE_CITIZEN_TIME = 5 * 60

# Must be lowercase.  The incoming hashtags will be lowercased before comparison.
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
	elif party.startswith("di"):
		color = "#c82864"
	elif party.startswith("de"):
		color = "#429EE2"
	elif party.startswith("p"):
		color = "#FFC0DB"  # Wikipedia page says just "pink", where the page about pink says "#FFC0DB"
	else:
		color = "#ffffff"

	return color


def contains_command(hashtags):
	for h in hashtags:
		if h.lower() in COMMAND_HASHTAGS:
			return True
	return False


# Search the tweet for a bird, and return the first one.
def find_bird(content, birdBack):
	content = content.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
	words = list(re.sub("[^\wäöüß]", " ",  content).split())
	for candidate in words:
		if candidate in birdBack.bJson:
			return candidate
	return None


# The core decisionmaker.  Gets a processed tweet (consumeTweet()) and
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
		print("{line}\nReceived tweet #{msg_id}:\n{tweet}"
			  .format(line="("*80, tweet=tweet, msg_id=self.prev_msg_id))

		# Boring stuff
		msg = dict()
		msg['content'] = tweet['content']
		msg['hashtags'] = tweet['hashtags']
		msg['id'] = self.prev_msg_id
		msg['image'] = tweet['profile_img']
		msg['name'] = tweet['userscreen']
		msg['retweet'] = tweet['retweet']
		msg['time'] = tweet['time']
		msg['twitterName'] = tweet['username']

		poli = self.pb.getPolitician(tweet['uid'])
		citi = self.tw.getCitizen(tweet['uid'])
		msg['byPoli'] = poli is not None  # FIXME: deprecated, remove

		# Resolve politician/citizen specifics
		if poli is not None:
			msg['poli'] = poli['pid']
			birds = self.handle_poli(tweet, msg)
		elif citi is not None:
			msg['poli'] = None
			birds = self.handle_citizen(citi, msg)
		else:
			print("Outdated tweet by no-longer citizen {}".format(tweet['uid']))
			birds = None

		# Make a sound
		if birds is None:
			print("=> drop tweet, DONE\n" + ")"*80)
			return
		cBird, pBird = birds
		msg['sound'] = generate_sound(tweet['content'], tweet['retweet'], cBird, pBird)

		# Send it
		self.sendingQueue.post(msg)
		print("Done with this tweet, DONE\n" + ")"*80)

	# For consistency.
	# noinspection PyMethodMayBeStatic
	def handle_citizen(self, citizen, msg):
		msg['partycolor'] = '#257E9C'  # some random, dark-ish blue
		# Don't define msg['refresh']
		return [citizen['birdId'], None]

	def handle_poli(self, tweet, msg):
		# Careful: we have a copy, so any changes due to setBird aren't reflected!
		poli = self.pb.getPolitician(tweet['uid'])
		if poli is None:
			print("No poli for tracked poli-uid {} found".format(tweet['uid']))
			return None

		msg['partycolor'] = party_to_color(poli['party'])
		pBird = poli['self_bird']

		# Check for any updates
		if contains_command(tweet['hashtags']):
			pid = poli['pid']
			bird_id = find_bird(tweet['content'], self.birdBack)
			if bird_id is None:
				print('I saw that command, but no valid bird!\n'
					  'pid={pid!r} content={ct}'
					  .format(ct=tweet['content'], pid=pid))
			else:
				print('politician "{}" ({}) gets new bird {}'
						.format(tweet['userscreen'], pid, bird_id))
				msg['refresh'] = dict()
				msg['refresh']['politicianId'] = pid
				msg['refresh']['birdId'] = bird_id
				self.pb.setBird(tweet['uid'], bird_id, actor='p')
				# Again, 'poli' is a copy, so it wasn't updated by the call to 'setBird'.
				pBird = bird_id

		# In case of 'refresh', poli already contains the update:
		return [poli['citizen_bird'], pBird]


COUNTER_PREV = 1


# Locking has to be done from the outside
# TODO: Shouldn't there be something for this in the stdlib?  Probably a class.
def poll_counter():
	global COUNTER_PREV
	COUNTER_PREV += 1
	return COUNTER_PREV


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
		if birdid not in self.birdBack.bJson:
			print("citizen user ignored, invalid bird: " + birdid)
			return

		with self.lock:
			if tid in self.citizens:
				entry = self.citizens[tid]
				print("Updating existing citizen's bird from {}".format(entry))
			else:
				print("Creating new citizen's bird")
				entry = dict()
				entry["userId"] = tid
				entry["party"] = 'neutral'
				self.citizens[tid] = entry
				# Even if a tweet comes in instantly, getCitizen syncs on
				# self.lock, so it's fine.  That's also why getCitizen() will
				# never see an incomplete citizen.
				self.twitter.register([tid], self.listener)

			entry["birdId"] = birdid
			token = poll_counter()
			entry["token"] = token
			print("Resulting citizen entry: {}".format(entry))
			timer = threading.Timer(REMOVE_CITIZEN_TIME,
									self._remove_citizen, [tid, token])
			# Don't prevent shutting down
			timer.daemon = True
			timer.start()

	def _remove_citizen(self, tid, token):
		with self.lock:
			print("Want to remove citizen {}, token {}".format(tid, token))
			if tid not in self.citizens:
				print("=> Already deleted (huh?)")
			elif self.citizens[tid]['token'] != token:
				print("=> Token mismatch, db has {}"
					  .format(self.citizens[tid]['token']))
			else:
				print("=> Yup")
				del self.citizens[tid]
			print("Remaining citizens: {}".format(self.citizens.keys()))

	def isPoli(self, uid):
		with self.lock:
			return str(uid) in self.poList
