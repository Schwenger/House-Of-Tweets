#!/usr/bin/env python3

from typing import List

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import tweepy
import json
import threading


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


class TweetPrinter(TweetConsumer):
    def consumeTweet(self, tweet: dict):
        print("incoming tweet {}".format(tweet))


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
        report['username'] = status["user"]["name"]
        report['userscreen'] = status["user"]["screen_name"]
        report['time'] = status["timestamp_ms"]
        report['profile_img'] = status["user"]["profile_image_url_https"]
        report['retweet'] = status["is_quote_status"]
        return report
    except KeyError:
        return None


class StreamListenerAdapter(StreamListener):
    def __init__(self, consumer: TweetConsumer, users: List[str]):
        super().__init__()
        # bypass the "parsing" done by StreamListener
        self.raw_data = None
        self.consumer = consumer
        self.desc = "{} ({} users)".format(users[:2], len(users))
        self.sensitive = set(users)

    def on_data(self, raw_data):
        if self.raw_data is not None:
            print("StreamListenerAdapter.raw_data was unclean.  Ignoring.")
        self.raw_data = raw_data
        ret = StreamListener.on_data(self, raw_data)
        self.raw_data = None
        return ret

    def on_connect(self):
        print("{}: on_connect".format(self.desc))

    def keep_alive(self):
        # Just ignore
        pass

    def on_tweet(self, tweet):
        print("{}: on_tweet".format(self.desc))
        self.consumer.consumeTweet(tweet)

    def on_status(self, status):
        if self.raw_data is None:
            print("ERROR: on_status called without going through on_data?!")
            return
        tweet = parse_tweet(json.loads(self.raw_data))
        if tweet is None:
            print("{}: on_tweet BROKEN! (skip)".format(self.desc))
        elif tweet['uid'] not in self.sensitive:
            print("{}: dropped irrelevant tweet from user {} at time {}"
                  .format(self.desc, tweet['uid'], tweet['time']))
        else:
            self.on_tweet(tweet)

    def on_exception(self, exception):
        print("{} on_exception {!r}".format(self.desc, exception))

    def on_delete(self, status_id, user_id):
        print("{} on_delete".format(self.desc))

    def on_event(self, status):
        print("{} on_event".format(self.desc))

    def on_direct_message(self, status):
        print("{} on_direct_message".format(self.desc))

    def on_friends(self, friends):
        print("{} on_friends".format(self.desc))

    def on_limit(self, track):
        print("{} on_limit".format(self.desc))

    def on_error(self, status_code):
        print("{} on_error: {}".format(self.desc, status_code))

    def on_timeout(self):
        print("{} on_timeout".format(self.desc))

    def on_disconnect(self, notice):
        print("{} on_disconnect: {}".format(self.desc, notice))
        """
        https://dev.twitter.com/docs/streaming-apis/messages#Disconnect_messages_disconnect
        """

    def on_warning(self, notice):
        print("{} on_warning: {}".format(self.desc, notice))


class RealTwitterInterface(TwitterInterface):
    def __init__(self):
        from credentials import consumer_key, consumer_secret, \
            access_key, access_secret
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_key, access_secret)
        self.streams = dict()
        self.lock = threading.RLock()
        self.api = tweepy.API(self.auth)

    def register(self, usernames, consumer: TweetConsumer) -> object:
        with self.lock:
            l = StreamListenerAdapter(consumer, usernames)
            stream = tweepy.Stream(self.auth, l)
            self.streams[tuple(usernames)] = stream
            stream.filter(follow=usernames, async=True)

    def deregister(self, usernames: List[str]):
        with self.lock:
            if tuple(usernames) not in self.streams:
                print("Tried to remove nonexistent usernames entry {}".format(usernames))
                return
            s = self.streams[tuple(usernames)]
            del self.streams[tuple(usernames)]
            s.disconnect()

    def resolve_name(self, username: str):
        try:
            return str(self.api.get_user(username).id)
        except Exception as e:
            print("Couldn't resolve username: " + str(e))
            return None


class FakeTwitterInterface(TwitterInterface):
    def __init__(self):
        self.consumers = dict()
        self.lock = threading.RLock()

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
                print("Tried to remove nonexistent usernames entry {}".format(usernames))
                return
            del self.consumers[tuple(usernames)]

    def resolve_name(self, username: str):
        raise AssertionError('FakeTwitterInterface is *only* for generating tweets.')
        # You only ever need to resolve a name when you're *about to* add a citizen,
        # so you can easily avoid that in test situations.


def manual_test_incoming():
    from time import sleep
    print("Reading from Twitter in stand-alone mode.")
    twi = RealTwitterInterface()
    print("Now following @HoT *and* Ben's throwaway account")
    twi.register(["4718199753"], TweetPrinter())
    twi.register(["774336282101178368"], TweetPrinter())
    print("sleeping...")
    sleep(50)
    print("Sleep nearly over!")
    sleep(10)
    print("Sleep over.  Unsubscribing Ben's throwaway account.")
    twi.deregister(["774336282101178368"])
    print("Kill with Ctrl-C")


# Only test for RealTwitterInterface.deregister
if __name__ == '__main__':
    manual_test_incoming()
