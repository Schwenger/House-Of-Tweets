#!/usr/bin/env python3

import json
import mq
from sys import argv
from time import sleep


def pull(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)


def check(tweets):
    assert len(tweets) > 0
    first_batch = tweets[0]
    assert len(first_batch) > 0
    first_tweet = first_batch[0]
    EXPECT_KEYS = {'content', 'hashtags', 'id', 'image', 'name',
                   'partycolor', 'retweet', 'sound', 'time', 'twitterName'}
    # Implicit assertion: first_tweet is a dict
    assert EXPECT_KEYS.issubset(first_tweet.keys()), first_tweet.keys()


# Waiting period, in milliseconds, between each sent batch
PERIOD_MS = 50


def vomit(tweets):
    print('Now vomiting {} tweet-batches all over the place.'.format(len(tweets)))
    q = mq.RealQueue('tweets')
    for batch in tweets:
        for t in batch:
            q.post([t])
            sleep(PERIOD_MS / 1000.0)


def transfer_file(filename):
    tweets = pull(filename)
    check(tweets)
    vomit(tweets)


if __name__ == '__main__':
    if len(argv) == 1:
        transfer_file('all_tweets.json')  # argv[0] is the program name
    elif len(argv) == 2:
        transfer_file(argv[1])  # argv[0] is the program name
    else:
        print('{}: need precisely one argument: the name of the tweets JSON file.'.format(argv[0]))
        exit(1)
