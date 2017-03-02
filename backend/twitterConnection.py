from birdBackend import BirdBackend
import re
import threading
from soundGenerator import generate_sound
import responseBuilder
from twitter import TwitterInterface, TweetConsumer
import mq
import mylog


# Seconds
REMOVE_CITIZEN_TIME = 5 * 60

# Must be lowercase.  The incoming hashtags will be lowercased before comparison.
COMMAND_HASHTAGS_DEFINITE = {'houseoftweets', 'house_of_tweets', 'house-of-tweets'}
COMMAND_HASHTAGS_ACKONLY = {'hot'}


def party_to_color(party: str):
	party = party.lower()

	if party is None:
		color = "#ffffff"
	elif party.startswith("c"):  # CDU/CSU
		color = "#000000"
	elif party.startswith("s"):  # SPD
		color = "#ff0000"
	elif party.startswith("g"):  # GRÜNE, Grün
		color = "#46962b"
	elif party.startswith("di"):  # DIE LINKE
		color = "#c82864"
	else:
		color = "#ffffff"

	return color


def contains_command(hashtags):
	for h in hashtags:
		if h.lower() in COMMAND_HASHTAGS_DEFINITE:
			return True
	for h in hashtags:
		if h.lower() in COMMAND_HASHTAGS_ACKONLY:
			return COMMAND_HASHTAGS_ACKONLY  # True-ish value, and self documenting arbitrary constant
	return False


# Search the tweet for a bird, and return the first one.
def find_bird(content, birdBack):
	words = list(re.sub("[^\w]", " ",  content).split())
	for candidate in words:
		bid = birdBack.getBid(candidate)
		if bid is not None:
			return bid
	return None


# The core decisionmaker.  Gets a processed tweet (consumeTweet()) and
class TwitterListener(TweetConsumer):
	def __init__(self, sendingQueue: mq.SendQueueInterface, tw,
				 politicianBackend, birdBack: BirdBackend):
		super().__init__()
		self.birdBack = birdBack
		self.sendingQueue = sendingQueue
		self.tw = tw
		self.pb = politicianBackend
		self.prev_msg_id = 42 - 1

	def consumeTweet(self, tweet):
		self.prev_msg_id += 1
		mylog.info("(" * 80)
		mylog.info("Received tweet #{msg_id}:".format(msg_id=self.prev_msg_id))
		mylog.debug(tweet)

		# Boring stuff
		msg = dict()
		msg['content'] = tweet['content']
		msg['hashtags'] = tweet['hashtags']
		msg['id'] = self.prev_msg_id
		msg['image'] = tweet['profile_img']
		msg['name'] = tweet['userscreen']
		msg['retweet'] = tweet['retweet'] or tweet['content'].startswith('RT ')
		msg['time'] = tweet['time']
		msg['twitterName'] = tweet['username']

		poli = self.pb.getPolitician(tweet['uid'])
		citi = self.tw.getCitizen(tweet['uid'])

		# Resolve politician/citizen specifics
		if poli is not None:
			mylog.info("This is definitely a politician.")
			msg['poli'] = poli['pid']
			birds = self.handle_poli(tweet, msg, poli)
		elif citi is not None:
			mylog.info("This is definitely a citizen.")
			msg['poli'] = None
			birds = self.handle_citizen(citi, msg)
		else:
			mylog.info("Outdated tweet by no-longer citizen {}".format(tweet['uid']))
			birds = None

		# Make a sound
		if birds is None:
			mylog.info("=> drop tweet, DONE")
			mylog.info(")" * 80)
			return
		cBird, pBird = birds
		msg['sound'] = generate_sound(tweet['content'], tweet['retweet'], cBird, pBird)

		# Send it
		self.sendingQueue.post(msg)
		mylog.info("Done with this tweet, DONE")
		mylog.info(")" * 80)

	# For consistency.
	# noinspection PyMethodMayBeStatic
	def handle_citizen(self, citizen, msg):
		msg['partycolor'] = '#257E9C'  # some random, dark-ish blue
		# Don't define msg['refresh']
		return [citizen['birdId'], None]

	def handle_poli(self, tweet, msg, poli):
		# Careful: 'poli' is a copy, so any changes due to setBird aren't reflected!

		msg['partycolor'] = party_to_color(poli['party'])
		msg['party'] = poli['party']
		pBird = poli['self_bird']
		# In case it changed, use the one provided by twitter
		handle = msg['twitterName']
		has_command = contains_command(tweet['hashtags'])

		# Check for any updates
		if 'house' in tweet['username'].lower() and tweet['content'].startswith('@'):
			mylog.warning("Ignoring my own tweet for commands, as it starts with '@'")
		elif has_command:
			pid = poli['pid']
			pBird_name = self.birdBack.getName(pBird)
			bird_id = find_bird(tweet['content'], self.birdBack)
			reply = None
			if bird_id is not None:
				# Ack
				bird_name = self.birdBack.getName(bird_id)
				mylog.info('politician "{}" ({}) gets new bird {}'
						   .format(tweet['userscreen'], pid, bird_id))
				msg['refresh'] = dict()
				msg['refresh']['politicianId'] = pid
				msg['refresh']['birdId'] = bird_id
				self.pb.setBird(pid, bird_id, actor='p')
				reply = responseBuilder.build_some_ack(handle, pBird_name, bird_name)
				# Again, 'poli' is a copy, so it wasn't updated by the call to 'setBird'.
				pBird = bird_id
			elif has_command != COMMAND_HASHTAGS_ACKONLY:
				# NACK
				mylog.warning('I saw that command, but no valid bird!')
				mylog.warning('pid={pid!r} content={ct}'
					          .format(ct=tweet['content'], pid=pid))
				reply = responseBuilder.build_some_nack(handle, pBird_name)
			if reply is not None:
				self.tw.twitter.maybe_reply(tweet['tweet_id'], reply)

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
		self.twitter.consumer_tweets = TwitterListener(self.queue, self, self.polBack, self.birdBack)
		self.twitter.register(followListPolitician, True)

	# Returns 'None' if not a citizen
	def getCitizen(self, cid):
		with self.lock:
			res = self.citizens.get(str(cid))
		return res

	def addCitizen(self, twittername, birdid, tid=None) -> str:
		if tid is None:
			tid = self.twitter.resolve_name(twittername)
		if tid is None:
			mylog.warning("citizen user ignored, invalid name: " + twittername)
			return "unknown-user"
		if self.polBack.getPolitician(tid) is not None:
			return "is-politician"
		if birdid not in self.birdBack.bJson:
			mylog.warning("citizen user ignored, invalid bird: " + birdid)
			return "unknown-bird"

		with self.lock:
			if tid in self.citizens:
				entry = self.citizens[tid]
				mylog.info("Updating existing citizen's bird from {}".format(entry))
			else:
				mylog.info("Creating new citizen's bird")
				entry = dict()
				entry["userId"] = tid
				entry["party"] = 'neutral'
				self.citizens[tid] = entry
				# Even if a tweet comes in instantly, getCitizen syncs on
				# self.lock, so it's fine.  That's also why getCitizen() will
				# never see an incomplete citizen.
				self.twitter.register([tid], False)

			entry["birdId"] = birdid
			token = poll_counter()
			entry["token"] = token
			mylog.debug("Resulting citizen entry: {}".format(entry))
			timer = threading.Timer(REMOVE_CITIZEN_TIME,
									self._remove_citizen_wrap, [tid, token])
			# Don't prevent shutting down
			timer.daemon = True
			timer.start()
		return None

	def _remove_citizen_wrap(self, tid, token):
		mylog.with_exceptions(self._remove_citizen, None, tid, token)

	def _remove_citizen(self, tid, token):
		with self.lock:
			mylog.info("Want to remove citizen {}, token {}".format(tid, token))
			if tid not in self.citizens:
				mylog.warning("=> Already deleted (huh?)")
			elif self.citizens[tid]['token'] != token:
				mylog.info("=> Token mismatch, db has {}"
					       .format(self.citizens[tid]['token']))
			else:
				mylog.info("=> Yup")
				self.twitter.deregister([tid])
				del self.citizens[tid]
				mylog.info("Remaining citizens: {}".format(self.citizens.keys()))

	def isPoli(self, uid):
		with self.lock:
			return str(uid) in self.poList
