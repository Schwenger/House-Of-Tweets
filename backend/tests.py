#!/usr/bin/env python3

import json
import mq
import twitter
import twitterConnection
import birdBackend
import politicianBackend

all_tests = []
MANUAL_TESTS = False


def test_mq():
    def run_with(maker):
        conn = maker("test_mq")
        if hasattr(conn, 'expect'):
            conn.expect([])
        conn.post("My lovely message")
        if hasattr(conn, 'expect'):
            conn.expect(["My lovely message"])
    print("Testing mq.PrintQueue:")
    run_with(mq.PrintQueue.new)
    if MANUAL_TESTS:
        print("[MANU] Testing mq.RealQueue. Check http://localhost:15672/#/queues/%2F/test_mq")
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
    expected = []
    for i in range(n):
        s = "Should be batch {batch}, message {i}/{n}" \
            .format(batch=batch, i=i, n=n)
        expected.append(s)
        batcher.post(s)
    time.sleep(mq.BATCH_TIMEOUT / 2.0)
    if hasattr(conn, 'expect'):
        conn.expect([])
    time.sleep(mq.BATCH_TIMEOUT)
    if hasattr(conn, 'expect'):
        # Expect precisely one message with all "parts" bundled up.
        conn.expect([expected])


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
    ids = {'HouseOfTweetsSB': '4718199753',
           '@HouseOfTweetsSB': '4718199753',
           '@MissesVlog': '50712079',
           'eeQu0Ae4': '774336282101178368',
           'SarcasticTester': '720224609560371201',
           'HopefullyNotARealTwitterAccount': None}
    twi = twitter.RealTwitterInterface()
    for (user, expect_id) in ids.items():
        actual_id = twi.resolve_name(user)
        # This really is how it's handled.
        # TODO: push str() call into resolve_name()
        if actual_id is not None:
            actual_id = str(actual_id)
        print('resolve {u} to {a!r} (expected {e!r})'
              .format(u=user, e=expect_id, a=actual_id))
        assert actual_id == expect_id

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


guess_counter = 0


def guess_sound():
    import os, soundGenerator
    global guess_counter
    guess_root = os.path.abspath(os.path.abspath(os.path.join(os.curdir, os.pardir)))
    s = "{root}/ext/sounds/processed/{time}_{id}.mp3" \
        .format(root=guess_root, time=soundGenerator.STARTUP, id=guess_counter)
    guess_counter += 1
    return s


def test_soundfile_guesser():
    global guess_counter
    # Ignore MANUAL_TESTS since we don't have side-effects anyway
    print("[MANU] Does this sound like a valid path to you?\n{}".format(guess_sound()))
    guess_counter = 0

all_tests.append(test_soundfile_guesser)


def test_twitter_citizenship():
    politicianBackend.check_writeback()
    politicianBackend.set_skip_writeback(True)
    politicianBackend.check_writeback()
    birdBack = birdBackend.BirdBackend()
    polBack = politicianBackend.PoliticianBackend()
    follow = ["4718199753", "774336282101178368"]
    queue = mq.PrintQueue("twitter_conn_test")
    fakeTwitter = twitter.FakeTwitterInterface()
    twi = twitterConnection.TwitterConnection(queue, follow, polBack, birdBack, fakeTwitter)
    queue.expect([])

    twi.addCitizen("Heinz1", "Katzastrophe", tid="12345678")
    queue.expect([])
    assert not twi.isPoli("12345678")
    assert twi.getCitizen("12345678") is None
    assert twi.citizens == dict()

    # Must be able to handle "decapitalization"
    twi.addCitizen("Heinz2", 'Ara', tid="12345679")
    queue.expect([])
    assert not twi.isPoli("12345679")
    assert twi.getCitizen("12345679") is not None
    assert twi.getCitizen("12345679")['birdId'] == 'ara'
    assert twi.citizens.keys() == {'12345679'}

    # FIXME: Citizen updates not implemented
    twi.addCitizen("Heinz3", 'zilpzalp', tid="12345679")
    queue.expect([])
    assert not twi.isPoli("12345679")
    assert twi.getCitizen("12345679") is not None
    assert twi.getCitizen("12345679")['birdId'] == 'ara'
    assert twi.citizens.keys() == {'12345679'}

    # Be able to deal with erroneous removals
    # noinspection PyProtectedMember
    twi._remove_citizen('123456')
    assert twi.citizens.keys() == {'12345679'}
    queue.expect([])

    # FIXME: Citizen delayed-removal not implemented

all_tests.append(test_twitter_citizenship)


def test_sound_gen():
    # Don't even attempt to prevent writing to disk.  Overwriting is perfectly
    # fine, as we don't overwrite anything important, and everything is in git.
    import soundGenerator

    actual = soundGenerator.generate_sound('Heyaloha', True, ['ara', 'zilpzalp'])
    expected = (guess_sound(), guess_sound(), 6000, 6000)
    assert actual == expected, (actual, expected)

    content = 'Ganz a doll langer aufgebrachter! Tweet!'
    actual = soundGenerator.generate_sound(content, False, ['wei\u00dfkopfseeadler', None])
    expected = (None, guess_sound(), 0, 10000)
    assert actual == expected, (actual, expected)
    soundGenerator.processed_tweets = 0

all_tests.append(test_sound_gen)


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
