#!/usr/bin/env python3

from typing import List
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import tweepy
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


class UpdatesConsumer(object):
    # Implementor must be able to handle calls from different threads.
    def updateShortpoll(self, username: str, reason: str):
        raise NotImplementedError("Should have implemented this")


class TwitterInterface(object):
    def register_longlived(self, ids: List[str]):
        raise NotImplementedError("Should have implemented this")

    def register_shortlived(self, id: str, username: str):
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


class UpdatesPrinter(UpdatesConsumer):
    def updateShortpoll(self, username: str, reason: str):
        mylog.info("update: {} on {}".format(username, reason))


def datetime_to_unix(dt):
    import datetime
    return int(dt.replace(tzinfo=datetime.timezone.utc).timestamp())


# Turn a very giant "Tweet" object (tweepy.models.Status)
# into a more easily spoofable and printable format.
def parse_tweet_status(status):
    # mylog.debug('Now parsing status {}'.format(status))
    try:
        report = dict()
        report['uid'] = status.user.id_str
        hh = status.entities["hashtags"]
        # For each element, only view 'text' subelement
        report['hashtags'] = []
        for h in hh:
            report['hashtags'].append(h['text'])
        report['content'] = status.text
        report['username'] = status.user.screen_name
        report['userscreen'] = status.user.name
        # Slap Twitter-developer for not delivering a 'timestamp_ms' property
        report['time'] = datetime_to_unix(status.created_at) * 1000
        report['tweet_id'] = status.id_str
        report['profile_img'] = status.user.profile_image_url_https
        if 'retweeted_status' in status.__dict__:
            # Actual "Retweet" (retweet with no additional text or media)
            sub = status.retweeted_status
            report['retweet'] = dict(
                # Skip uid (available on request!)
                # Skip hashtags (available on request!)
                content=sub.text,
                username=sub.user.screen_name,
                userscreen=sub.user.name,
                # Skip time (available on request -- but difficult for quotes, see below)
                tweet_id=sub.id_str,
                profile_img=status.user.profile_image_url_https,
                # No recursive retweet detection -- would require POST requests.
                )
        elif 'quoted_status' in status.__dict__:
            # "Quote" (retweet with some additional text or media)
            # Dear tweepy, why don't you parse this JSON?!
            # I would create a new issue, but it's "no longer maintained" anyway.
            sub = status.quoted_status
            report['retweet'] = dict(
                # Skip uid (available on request!)
                # Skip hashtags (available on request!)
                content=sub['text'],
                username=sub['user']['screen_name'],
                userscreen=sub['user']['name'],
                # Skip time (available on request -- but would need non-trivial parsing)
                tweet_id=sub['id_str'],
                profile_img=sub['user']['profile_image_url_https'],
                )
        # else: not a retweet in either meaning.
        # For initial compatibility with the current tests: throw away most of the info.
        report['retweet'] = report.get('retweet') is not None
        return report
    except (KeyError, AttributeError) as e:
        mylog.debug('Failed to parse status {}'.format(status))
        mylog.error('Something when wrong while parsing status: {}'.format(e))
        return None


# Reduce the implementation workload for the "tweet consumer" by filtering out
# irrelevant retweets and handling all the tweepy requirements.
# Also, don't require a 'StreamListener' implementation from them.
class StreamListenerAdapter(StreamListener):
    def __init__(self, consumer: TweetConsumer, users: List[str], restarter):
        super().__init__()
        self.consumer = consumer
        self.desc = "{} ({} users)".format(list(users)[:2], len(users))
        self.sensitive = set(users)
        self.restarter = restarter

    # Intercept on_data calls because we want the raw data later on.
    def on_data(self, raw_data):
        if raw_data is None:
            mylog.error("Tweepy says raw_data=None.  Wat.  Dropping tweet, or whatever it was.")
            return
        return StreamListener.on_data(self, raw_data)

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
        tweet = parse_tweet_status(status)
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


# We have a budget of 180 calls per 15 minutes, that's one call per 3 seconds.
# Allow up to two citizens.
# Since that's ridiculously small, hope that we can get away with 200 per 15 minutes.
# Formula:
# (15 minutes * 60 seconds per minutes * 2 calls per wakeup) / 200 calls
# = 9 seconds per wakeup
SHORT_POLL_PERIOD = 9.1


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

        self.consumer_tweets = TweetPrinter()
        self.consumer_updates = UpdatesPrinter()

        creds = CREDENTIALS[self.key]
        self.auth = OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
        self.auth.set_access_token(creds['access_key'], creds['access_secret'])
        # self.streams is a dict of:
        #   K: tuple of Twitter IDs
        #   V: handler, the "TweetConsumer" object
        # Unless you provide the same TweetConsumer object multiple times,
        # it appears at most once in this container.
        self.streams = dict()
        self.lock = threading.RLock()
        self.api = tweepy.API(self.auth)
        # self.short_poll is a list of:
        #   Entries, which are represented by a dict, which should have been a struct:
        #     'user': string, required, Twitter ID
        #     'name': string, required, screen name
        #     'last_id': string, optional, textual representation of the ID of the most recent Tweet
        # Unless you provide the same TweetConsumer object multiple times,
        # it appears at most once in this container.
        self.short_poll = []

        # Start the short-poll thread
        self.run_short_poll_wrap()

    def register_longlived(self, ids: List[str]):
        with self.lock:
            self.streams[tuple(ids)] = RestartingStream(self.consumer_tweets, ids, self.auth)

    def register_shortlived(self, id: str, username: str):
        with self.lock:
            mylog.info('Adding short-poll for {}'.format(id))
            # Note: no 'last_tweet' set.
            self.short_poll.append({'user': id, 'name': username})

    def deregister(self, usernames: List[str]):
        with self.lock:
            if tuple(usernames) in self.streams:
                s = self.streams[tuple(usernames)]
                del self.streams[tuple(usernames)]
                s.disconnect()
            else:
                # Technically, we don't have any timing guarantees about
                # when run_short_poll can prune the list down to size 2.
                # Practically, if we hit this limit, something has gone very wrong.
                assert len(self.short_poll) < 100, self.short_poll

                # Split list based on predicate "Should it be removed?"
                users_pruned = []
                users_passed = []
                for e in self.short_poll:
                    l = users_pruned if e['user'] in usernames else users_passed
                    l.append(e)

                if len(users_pruned) != len(usernames):
                    mylog.warning("Tried to remove nonexistent usernames entries.")
                    mylog.warning("  Actually pruned: {}", users_pruned)
                    mylog.warning("  Wanted to prune: {}", usernames)
                if len(users_pruned) > 0:
                    mylog.info("Some short-polls removed: {}".format(users_pruned))
                    self.short_poll = users_passed
                    for e in users_pruned:
                        self.consumer_updates.updateShortpoll(e['name'], 'del-timeout')
                return

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
            self.api.update_status(status=content, in_reply_to_status_id=tweet_id)
        mylog.info("-" * 40)

    def run_short_poll_wrap(self):
        # TODO: Think of a safer way to do the restarting.
        try:
            mylog.with_exceptions(self.run_short_poll)
        finally:
            # Precisely one execution per iteration returns without exception
            timer = threading.Timer(SHORT_POLL_PERIOD, self.run_short_poll_wrap)
            timer.daemon = True
            timer.start()

    # Poll tweets of a *single* citizen
    def poll_user(self, e):
        query_params = dict(user_id=e['user'], count=2)
        seen_tweets = []  # Collect string representation of Tweet IDs
        if 'last_id' in e:
            query_params['since_id'] = e['last_id']
            is_new = False
            seen_tweets.append(e['last_id'])
        else:
            is_new = True
        mylog.debug('[POLL] on REST with {} (new={})'.format(query_params, is_new))
        statuses = self.api.user_timeline(**query_params)
        for status in statuses:
            tweet = parse_tweet_status(status)
            seen_tweets.append(tweet['tweet_id'])
            if not is_new:
                self.consumer_tweets.consumeTweet(tweet)
        assert len(seen_tweets) > 0, e
        # Oh god.  I'm so sorry.
        e['last_id'] = str(max([int(tid) for tid in seen_tweets]))
        if is_new:
            self.consumer_updates.updateShortpoll(e['name'], 'succ-firstpoll')

    # Poll tweets of *all* citizens
    def run_short_poll(self):
        # Need to hold the lock *all* the time, as the self.api object might be modified
        # by the other objects.
        # WARNING: This opens up a convoluted but definite attack vector:
        # If you can manage to delay a REST call for a very long time, then the backend grinds to a halt.
        # Then again, with this level of network control you can always do that.
        # This is why I actually ignore this attack vector.
        with self.lock:
            if len(self.short_poll) > 2:
                retained = self.short_poll[-2:]  # The two last entries
                dropped = self.short_poll[:-2]  # Other entries
                mylog.warning('Lots of citizens!  Dropping {}, retaining {} ...'.format(dropped, retained))
                for e in dropped:
                    self.consumer_updates.updateShortpoll(e['name'], 'del-toomany')
                self.short_poll = retained
            assert len(self.short_poll) <= 2, self.short_poll
            for e in self.short_poll:
                self.poll_user(e)


class FakeTwitterInterface(TwitterInterface):
    def __init__(self):
        self.consumer_tweets = TweetPrinter()
        self.consumer_updates = UpdatesPrinter()  # Can't be used for testing
        self.user_blocks = set()
        self.lock = threading.RLock()
        self.replies = []

    def send(self, fake_tweet: dict):
        tid = str(fake_tweet['uid'])
        with self.lock:
            # Would have sent a tweet twice if the setup is bad,
            # just like in reality.
            for users in self.user_blocks:
                if tid in users:
                    self.consumer_tweets.consumeTweet(fake_tweet)

    def register_longlived(self, ids: List[str]):
        self.register_(ids)

    def register_shortlived(self, id: str, username: str):
        self.register_([id])

    def register_(self, usernames):
        with self.lock:
            self.user_blocks.add(tuple(usernames))

    def deregister(self, usernames: List[str]):
        with self.lock:
            if tuple(usernames) not in self.user_blocks:
                mylog.warning("Tried to remove nonexistent usernames entry {}".format(usernames))
                return
            self.user_blocks.remove(tuple(usernames))
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
    mylog.info("Reading from Twitter in stand-alone mode.")
    twi = RealTwitterInterface()
    mylog.info("Now following @HoT *and* Ben's throwaway account")
    # If commented out, add 'while True: input()' at the very end:
    twi.register_longlived(["4718199753"])  # HouseOfTweetsSB
    twi.register_shortlived("774336282101178368", "eeQu0Ae4")
    twi.register_shortlived("139407967", "SevimDagdelen")
    mylog.info("Kill with Ctrl-C")
    # while True:
    #     input()


# Only test for RealTwitterInterface
if __name__ == '__main__':
    manual_test_incoming()
