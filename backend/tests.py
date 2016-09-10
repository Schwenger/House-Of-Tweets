#!/usr/bin/env python3

import json
import mq
import twitter
import twitterConnection
import politicianBackend

all_tests = []
MANUAL_TESTS = False


def test_mq():
    def run_with(maker):
        conn = maker("test_mq")
        conn.post("My lovely message")
    print("Testing mq.PrintQueue:")
    run_with(mq.PrintQueue.new)
    if MANUAL_TESTS:
        print("Testing mq.RealQueue. MANUAL: http://localhost:15672/#/queues/%2F/test_mq")
        run_with(mq.RealQueue.new)
    else:
        print("SKIP RealQueue access")

all_tests.append(test_mq)


def test_batching_x(n, batch):
    import time
    # from datetime import datetime
    print("Testing batching.TweetBatcher:")
    conn = mq.PrintQueue.new('test_batching')
    batcher = mq.Batcher(conn)
    # argument should be a tweet, but who cares
    for i in range(n):
        batcher.add("Should be batch {batch}, message {i}/{n}"
                    .format(batch=batch, i=i, n=n))
    time.sleep(mq.BATCH_TIMEOUT / 2.0)
    assert conn.received == 0
    time.sleep(mq.BATCH_TIMEOUT)
    assert conn.received == 1


def test_batching1():
    test_batching_x(1, 1)

all_tests.append(test_batching1)


def test_batching7():
    test_batching_x(7, 2)

all_tests.append(test_batching7)


def test_parse_tweet():
    with open("raw_tweet.json", "r") as fp:
        status = json.load(fp)
    actual = twitter.parse_tweet(status)
    # Somewhat fragile test, but at least it shows you what the internal format looks like
    expected = {'content': 'Blarghi v2.0 #Improved #Harder #Faster #Stronger https:\\/\\/t.co\\/qzF99STdcU',
                'profile_img': 'https:\\/\\/pbs.twimg.com\\/profile_images\\/774232619248746500\\/5wvBHiHp_normal.jpg',
                'userscreen': 'HouseOfTweetsSB',
                'hashtags': ['Improved', 'Harder', 'Faster', 'Stronger'],
                'username': 'HouseOfTweets',
                'time': '1473446404525',
                'uid': 4718199753,
                'retweet': True,
                'tweetId': 774316458742583296}
    assert actual == expected

all_tests.append(test_parse_tweet)


def test_name_resolution():
    twi = twitter.RealTwitterInterface()
    for u in ['HouseOfTweetsSB', '@HouseOfTweetsSB', '@MissesVlog', 'eeQu0Ae4',
              'SarcasticTester', 'HopefullyNotARealTwitterAccount']:
        print('resolve {}={!r}'.format(u, twi.resolve_name(u)))

all_tests.append(test_name_resolution)


def test_party_color():
    known_results = {'GR\u00dcNE': '#00cc00', 'CDU': '#000000',
                     'CSU': '#000000', 'SPD': '#ff0000',
                     'DIE LINKE': '#c82864'}
    for (party, expected) in known_results.items():
        actual = twitterConnection.party_to_color(party)
        assert actual == expected

all_tests.append(test_party_color)


def test_command_recognition():
    for h in ['HouseOfTweets', 'HoT', 'HOT']:
        assert twitterConnection.contains_command([h])
        assert twitterConnection.contains_command(['shit', h, 'what'])
    for h in ['something', 'hottie', 'HouseOfTwats']:
        assert not twitterConnection.contains_command([h])
        assert not twitterConnection.contains_command(['shit', h, 'what'])

all_tests.append(test_command_recognition)


def test_bird_recognition():
    from birdBackend import BirdBackend
    results = {'Ich will ein Ara sein!!': 'ara',
               'Ich auch!': None,
               "Gibt's für mich einen ZilpZalp?!": 'zilpzalp',
               'Zaunkönig auch?': 'zaunkoenig',
               'How about #Weißkopfseeadler?!': 'wei\u00dfkopfseeadler',
               'Ick bin ein zaunkoenig #obamalincoln': 'zaunkoenig',
               'Für mich einen Paradiesvogel': None,
               'Hey! Paradiesvogel!': None,
               'Menno': None,}
    birdBack = BirdBackend()
    for (input, expected) in results.items():
        actual = twitterConnection.find_bird(input, birdBack)
        if actual is not None:
            new_actual = actual[0]
            assert new_actual is not None
            actual = new_actual
        assert expected == actual, (input, expected, actual)

all_tests.append(test_bird_recognition)


def test_twitter_listener():
    politicianBackend.check_writeback()
    politicianBackend.set_skip_writeback(True)
    politicianBackend.check_writeback()

all_tests.append(test_twitter_listener)


def test_all():
    # This might show weird behavior if you modify MANUAL_TESTS by hand
    print('[TEST] -- Running all tests (MANUAL_TESTS={}) --'.
          format(MANUAL_TESTS))
    for t in all_tests:
        print("[TEST] {}".format(t))
        t()
        print("[DONE] {}".format(t))
    print('[DONE] -- Done with all tests --')

if __name__ == '__main__':
    test_all()
