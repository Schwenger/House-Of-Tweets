#!/usr/bin/env python3

from typing import List
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import tweepy
import json
import mylog
import threading


# If a crashing bug in tweepy happens,
# after how many seconds shall we try again?
RESPAWN_PERIOD = 15

# List of all keys that are allowed to actually post something on Twitter.
MAY_POST = ['production_responder']


class TweetConsumer(object):
    def consumeTweet(self, tweet: dict):
        raise NotImplementedError("Should have implemented this")


class TwitterInterface(object):
    def register(self, usernames: List[str], listener: TweetConsumer):
        raise NotImplementedError("Should have implemented this")

    def deregister(self, usernames: List[str]):
        raise NotImplementedError("Should have implemented this")

    def resolve_name(self, username: str):
        raise NotImplementedError("Should have implemented this")

    # 'Maybe' because it's the responsibility of this method to check
    # whether we should actually send this to Twitter.
    # (I.e., check whether we're in test mode or in silent mode.)
    def maybe_reply(self, tweet_id: str, content: str):
        raise NotImplementedError("Should have implemented this")


class TweetPrinter(TweetConsumer):
    def consumeTweet(self, tweet: dict):
        mylog.info("incoming tweet {}".format(tweet))


# Turn a giant "Tweet" JSON into a more easily spoofable and printable format.
def parse_tweet(status):
    try:
        report = dict()
        report['uid'] = str(status["user"]["id"])
        hh = status["entities"]["hashtags"]
        # For each element, only view 'text' subelement
        report['hashtags'] = []
        for h in hh:
            report['hashtags'].append(h['text'])
        report['content'] = status["text"]
        report['username'] = status["user"]["screen_name"]
        report['userscreen'] = status["user"]["name"]
        report['time'] = status["timestamp_ms"]
        report['tweet_id'] = status["id_str"]
        report['profile_img'] = status["user"]["profile_image_url_https"]
        report['retweet'] = status["is_quote_status"]
        return report
    except KeyError:
        return None


# Reduce the implementation workload for the "tweet consumer" by filtering out
# irrelevant retweets and handling all the tweepy requirements.
# Also, don't require a 'StreamListener' implementation from them.
class StreamListenerAdapter(StreamListener):
    def __init__(self, consumer: TweetConsumer, users: List[str], restarter):
        super().__init__()
        # bypass the "parsing" done by StreamListener
        self.raw_data = None
        self.consumer = consumer
        self.desc = "{} ({} users)".format(list(users)[:2], len(users))
        self.sensitive = set(users)
        self.restarter = restarter

    # Intercept on_data calls because we want the raw data later on.
    def on_data(self, raw_data):
        if self.raw_data is not None:
            mylog.warning("StreamListenerAdapter.raw_data was unclean.  Ignoring.")
        self.raw_data = raw_data
        ret = StreamListener.on_data(self, raw_data)
        self.raw_data = None
        return ret

    def on_connect(self):
        mylog.info("{}: on_connect".format(self.desc))

    def keep_alive(self):
        # Just ignore
        pass

    def on_tweet(self, tweet):
        mylog.info("{}: on_tweet".format(self.desc))
        self.consumer.consumeTweet(tweet)

    # A tweet arrived.  The retweet filtering happens here.
    def on_status(self, status):
        if self.raw_data is None:
            mylog.error("on_status called without going through on_data?!")
            return
        tweet = parse_tweet(json.loads(self.raw_data))
        if tweet is None:
            mylog.error("{}: on_tweet BROKEN! (skip)".format(self.desc))
        elif tweet['uid'] not in self.sensitive:
            mylog.info("{}: dropped irrelevant tweet from user {} at time {}"
                       .format(self.desc, tweet['uid'], tweet['time']))
        else:
            self.on_tweet(tweet)

    def on_exception(self, exception):
        # Fun fact: even if no thread is runnable,
        # the existence of a Timer keeps Python alive.
        threading.Timer(RESPAWN_PERIOD, self.restarter.restart_now).start()
        # tweepy has lots of bugs.  Backend and tweepy exception will
        # result in this code being called, so use it as a trampoline.
        # Log it 'only' as a warning, since if we get here, this isn't too bad anyway.
        mylog.warning("{} on_exception!  Trying to print it:".format(self.desc))
        mylog.warning("(You'll see the same error immediately again, but don't"
                      " worry, I'm a Phoenix, I'll get revived in a few seconds.)")
        mylog.warning(exception)

    def on_delete(self, status_id, user_id):
        mylog.info("{} on_delete".format(self.desc))

    def on_event(self, status):
        mylog.info("{} on_event".format(self.desc))

    def on_direct_message(self, status):
        mylog.info("{} on_direct_message".format(self.desc))

    def on_friends(self, friends):
        mylog.info("{} on_friends".format(self.desc))

    def on_limit(self, track):
        mylog.info("{} on_limit".format(self.desc))

    def on_error(self, status_code):
        mylog.info("{} on_error: {}".format(self.desc, status_code))

    def on_timeout(self):
        mylog.info("{} on_timeout".format(self.desc))

    def on_disconnect(self, notice):
        mylog.info("{} on_disconnect: {}".format(self.desc, notice))
        """
        https://dev.twitter.com/docs/streaming-apis/messages#Disconnect_messages_disconnect
        """

    def on_warning(self, notice):
        mylog.warning("{} on_warning: {}".format(self.desc, notice))


# tweepy has lots of bugs.  This is essentially a wrapper that automatically
# restarts on tweepy- or backend-induced errors.  Note that Twitter error
# codes and connectivity issues are already handled by tweepy, so no need
# for any sophisticated algorithms here.
class RestartingStream:
    def __init__(self, consumer, usernames, auth):
        self.active = True
        self.s = None
        self.consumer = consumer
        self.usernames = usernames
        self.auth = auth
        self.lock = threading.RLock()

        self.restart_now()

    def restart_now(self):
        mylog.with_exceptions(self._restart_now)

    def _restart_now(self):
        with self.lock:
            if not self.active:
                return
            if self.s is not None:
                self.s.disconnect()
            l = StreamListenerAdapter(self.consumer, self.usernames, self)
            self.s = tweepy.Stream(self.auth, l)
            self.s.filter(follow=self.usernames, async=True)

    def disconnect(self):
        with self.lock:
            self.active = False
            if self.s is None:
                return
            self.s.disconnect()
            self.s = None


def show_usage(keys):
    from sys import exit
    mylog.error('Start it like this:')
    mylog.error('( cd backend && ./startBackend.py ${SOME_KEY} )')
    mylog.error('Where the following values are accepted for ${SOME_KEY}:')
    mylog.error('{}'.format(keys))
    exit(1)


class RealTwitterInterface(TwitterInterface):
    def __init__(self):
        # Read argv to determine which credentials to use
        from credentials import CREDENTIALS
        from sys import argv

        show_keys = set(CREDENTIALS.keys())  # Copy to be extra safe
        if len(argv) != 2:
            mylog.error('Must specify exactly one argument, but {} provided.'.format(len(argv) - 1))
            show_usage(show_keys)
        self.key = argv[1]
        if self.key not in CREDENTIALS:
            mylog.error('Unknown key {} provided.'.format(self.key))
            show_usage(show_keys)

        creds = CREDENTIALS[self.key]
        self.auth = OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
        self.auth.set_access_token(creds['access_key'], creds['access_secret'])
        self.streams = dict()
        self.lock = threading.RLock()
        self.api = tweepy.API(self.auth)

    def register(self, usernames, consumer: TweetConsumer) -> object:
        with self.lock:
            self.streams[tuple(usernames)] = RestartingStream(consumer, usernames, self.auth)

    def deregister(self, usernames: List[str]):
        with self.lock:
            if tuple(usernames) not in self.streams:
                mylog.warning("Tried to remove nonexistent usernames entry {}".format(usernames))
                return
            s = self.streams[tuple(usernames)]
            del self.streams[tuple(usernames)]
            s.disconnect()

    def resolve_name(self, username: str):
        try:
            return str(self.api.get_user(username).id)
        except Exception as e:
            mylog.warning("Couldn't resolve username '{}': {}".format(username, e))
            return None

    def maybe_reply(self, tweet_id: str, content: str):
        mylog.info("-" * 40)
        mylog.info("About to respond ({} chars): {}".format(len(content), content))
        if self.key not in MAY_POST:
            mylog.info("Not posting this reply, as key {} is not permitted.  Try one of {} instead."
                       .format(self.key, MAY_POST))
        else:
            mylog.info("Actually writing to Twitter!")
            # self.api.update_status(status=content, in_reply_to_status_id=tweet_id)
            mylog.error("Hah!  Gotcha.  :notyet:")
        mylog.info("-" * 40)


class FakeTwitterInterface(TwitterInterface):
    def __init__(self):
        self.consumers = dict()
        self.lock = threading.RLock()
        self.replies = []

    def send(self, fake_tweet: dict):
        tid = str(fake_tweet['uid'])
        with self.lock:
            for (users, consumer) in self.consumers.items():
                if tid in users:
                    consumer.consumeTweet(fake_tweet)

    def register(self, usernames, consumer: TweetConsumer) -> object:
        with self.lock:
            self.consumers[tuple(usernames)] = consumer

    def deregister(self, usernames: List[str]):
        with self.lock:
            if tuple(usernames) not in self.consumers:
                mylog.warning("Tried to remove nonexistent usernames entry {}".format(usernames))
                return
            del self.consumers[tuple(usernames)]
            mylog.info("Successfully removed {}".format(usernames))

    def resolve_name(self, username: str):
        raise AssertionError('FakeTwitterInterface is *only* for generating tweets.')
        # You only ever need to resolve a name when you're *about to* add a citizen,
        # so you can easily avoid that in test situations.

    def maybe_reply(self, tweet_id: str, content: str):
        self.replies.append((tweet_id, content))

    def expect(self, replies_expect):
        assert self.replies == replies_expect, (self.replies, replies_expect)
        self.replies = []


def manual_test_incoming():
    from time import sleep
    mylog.info("Reading from Twitter in stand-alone mode.")
    twi = RealTwitterInterface()
    mylog.info("Now following @HoT *and* Ben's throwaway account")
    twi.register(["4718199753"], TweetPrinter())
    twi.register(["774336282101178368"], TweetPrinter())
    mylog.info("sleeping...")
    sleep(50)
    mylog.info("Sleep nearly over!")
    sleep(10)
    mylog.info("Sleep over.  Unsubscribing Ben's throwaway account.")
    twi.deregister(["774336282101178368"])
    mylog.info("Kill with Ctrl-C")


# Only test for RealTwitterInterface.deregister
if __name__ == '__main__':
    manual_test_incoming()
