#!/usr/bin/env python3

import birdBackend
import json
import mq
import mylog
import os
import politicianBackend
import responseBuilder
import soundGenerator
import time
import twitter
import twitterConnection

all_tests = []

RUN_SLOW_TESTS = 'CONTINUOUS_INTEGRATION' in os.environ

# Stay away from the official maximum 140 in order to have a safety margin.
MAX_RESPONSE_LENGTH = 130


def test_mq():
    def run_with(maker):
        conn = maker("test_mq")
        if hasattr(conn, 'expect'):
            conn.expect([])
        for s in ["My lovely message", "Ümläöts Partyß! Or … what¿"]:
            conn.post(s)
            if hasattr(conn, 'expect'):
                conn.expect([s])
    mylog.info("Testing mq.PrintQueue:")
    run_with(mq.PrintQueue.new)
    mylog.warning("[MANU] Testing mq.RealQueue. Check http://localhost:15672/#/queues/%2F/test_mq")
    run_with(mq.RealQueue.new)

all_tests.append(test_mq)


def test_json_sanity():
    obj = {'füßli … thing': 'Schemel¿', 'Köpflı': ['ohr', 'ohr', 'auge', 'stroh']}
    expected = '{\n  "K\\u00f6pfl\\u0131": [\n    "ohr",\n    "ohr",\n    "auge",\n    "stroh"\n  ],' \
               '\n  "f\\u00fc\\u00dfli \\u2026 thing": "Schemel\\u00bf"\n}'
    actual = json.dumps(obj, sort_keys=True, indent=2)
    assert actual == expected, (actual, expected)

all_tests.append(test_json_sanity)


def test_batching_x(n, batch):
    if not RUN_SLOW_TESTS:
        mylog.warning("[SKIP] Skipping slow test")
        return

    mylog.info("Testing batching.TweetBatcher:")
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

    expected = 'Check second run'
    batcher.post(expected)
    time.sleep(mq.BATCH_TIMEOUT / 2.0)
    if hasattr(conn, 'expect'):
        conn.expect([])
    time.sleep(mq.BATCH_TIMEOUT)
    if hasattr(conn, 'expect'):
        batch = [expected]
        all_batches = [batch]
        conn.expect(all_batches)


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
                'userscreen': 'HouseOfTweets',
                'hashtags': ['Improved', 'Harder', 'Faster', 'Stronger'],
                'username': 'HouseOfTweetsSB',
                'time': '1473446404525',
                'tweet_id': '774316458742583296',
                'uid': '4718199753',
                'retweet': True}
    assert actual == expected

all_tests.append(test_parse_tweet)


def test_responses():
    responses = []
    responses.extend(responseBuilder.build_worst_acks())
    responses.extend(responseBuilder.build_worst_nacks())
    # Not a dict to preserve order
    lengths = [(len(r), r) for r in responses]
    mylog.info("Worst-case response lengths: {}"
               .format([len(r) for r in responses]))
    for (l, r) in lengths:
        assert l <= MAX_RESPONSE_LENGTH, (l, r)

all_tests.append(test_responses)


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
        mylog.info('resolve {u} to {a!r} (expected {e!r})'
                   .format(u=user, e=expect_id, a=actual_id))
        assert actual_id == expect_id

all_tests.append(test_name_resolution)


def test_party_color():
    # Currently, these are *all* parties in our dataset:
    # CDU, CSU, Demokraten, DIE LINKE, GR\u00dcNE, Gr\u00fcn,
    # Parti socialiste, SPD
    known_results = {'GR\u00dcNE': '#00cc00', 'CDU': '#000000',
                     'CSU': '#000000', 'SPD': '#ff0000',
                     'DIE LINKE': '#c82864',
                     'Demokraten': '#429EE2',
                     'Parti socialiste': '#FFC0DB'}
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
               'How about #Weißkopfseeadler?!': 'weisskopfseeadler',
               'Ick bin ein zaunkoenig #obamalincoln': 'zaunkoenig',
               'Für mich einen Paradiesvogel': None,
               'Hey! Paradiesvogel!': None,
               'Menno': None,
               'Ich will ein ara sein! #HoT': 'ara',
               'Ara? So ein Blödsinn, ich bin eine Amsel! #HoT': 'ara',
               'Ich bin eine Amsel! #HoT': 'amsel',
               '#HoT #Amsel': 'amsel',
               'Ara!!! #HoT': 'ara',
               '#Ara #HoT': 'ara',
               'Party@Ara! Voll der Vogel11! #HoT': 'ara',
               'Amsel#1 mein Lieber! #houseoftweets': 'amsel',
               'Frei wie ein Vogel! #houseoftweets': None,
               }
    birdBack = BirdBackend()
    for (input, expected) in results.items():
        actual = twitterConnection.find_bird(input, birdBack)
        assert expected == actual, (input, expected, actual)

all_tests.append(test_bird_recognition)


def long_wait(secs):
    mylog.info("Waiting for {} seconds.  Note that Travis kills".format(secs))
    mylog.info("you after 600 seconds of no output.")
    time.sleep(secs)


# Test whether adding / updating / deleting citizens works as intended.
def test_twitter_citizenship():
    # This test won't change anything about the politicians,
    # but still, better play it safe.
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
    twi.addCitizen("Heinz2", 'ara', tid="12345679")
    queue.expect([])
    assert not twi.isPoli("12345679")
    assert twi.getCitizen("12345679") is not None
    assert twi.getCitizen("12345679")['birdId'] == 'ara'
    assert twi.citizens.keys() == {'12345679'}

    # Be able to deal with erroneous removals
    # noinspection PyProtectedMember
    twi._remove_citizen('123456', 666)  # token of the beast
    assert twi.citizens.keys() == {'12345679'}
    queue.expect([])

    if RUN_SLOW_TESTS:
        mylog.info("This wakeup should be completely silent.")
        long_wait(twitterConnection.REMOVE_CITIZEN_TIME / 2)

    twi.addCitizen("Heinz3", 'zilpzalp', tid="12345679")
    queue.expect([])
    assert not twi.isPoli("12345679")
    assert twi.getCitizen("12345679") is not None
    assert twi.getCitizen("12345679")['birdId'] == 'zilpzalp'
    assert twi.citizens.keys() == {'12345679'}

    if not RUN_SLOW_TESTS:
        mylog.warning("The slow part of test_twitter_citizenship().")
        mylog.warning("You might see several stray 'citizen removed' messages.")
        return

    mylog.info("This wakeup should be a no-op.")
    long_wait(twitterConnection.REMOVE_CITIZEN_TIME / 2 + 10)
    queue.expect([])
    assert not twi.isPoli("12345679")
    assert twi.getCitizen("12345679") is not None
    assert twi.getCitizen("12345679")['birdId'] == 'zilpzalp'
    assert twi.citizens.keys() == {'12345679'}

    mylog.info("This wakeup should remove it, as citizen deletion")
    mylog.info("has been deferred when the bird was updated.")
    long_wait(twitterConnection.REMOVE_CITIZEN_TIME / 2 + 10)
    queue.expect([])
    assert not twi.isPoli("12345679")
    assert twi.getCitizen("12345679") is None
    assert twi.citizens.keys() == set()

all_tests.append(test_twitter_citizenship)


def test_sound_gen():
    # Don't even attempt to prevent writing to disk.  Overwriting is perfectly
    # fine, as we don't overwrite anything important, and everything is in git.
    mylog.warning("Please check by hand whether this generates the file on the")
    mylog.warning("first call and uses the cached version on the second:")
    actual = soundGenerator.generate_sound('Cheerio, buddy', False, 'amsel', 'amsel')
    # Set as 'warning' so that the user always sees both (or neither).
    mylog.warning("(end of manual part)")
    path_amsel = os.path.join(soundGenerator.SOUND_ROOT, 'processed', 'amsel-neutral-10000.mp3')
    desc_amsel = {'natural': path_amsel, 'bid': 'amsel'}
    expected = {'duration': 10000, 'citizen': desc_amsel, 'poli': desc_amsel}
    assert actual == expected, (actual, expected)

    content = "How can mirrors be real if our eyes aren't real?"
    actual = soundGenerator.generate_sound(content, True, 'zilpzalp', None)
    path_zz = os.path.join(soundGenerator.SOUND_ROOT, 'processed', 'zilpzalp-fragend-r-12000.mp3')
    desc_zz = {'natural': path_zz, 'bid': 'zilpzalp'}
    expected = {'duration': 12000, 'citizen': desc_zz, 'poli': None}
    assert actual == expected, (actual, expected)
    soundGenerator.processed_tweets = 0

all_tests.append(test_sound_gen)


def test_mood_detection():
    battery = {'It is dark here': 'neutral',
               'Why is it SO DAMN DARK': 'aufgebracht',
               'Who turned off the light?!': 'aufgebracht',
               'Who turned off the light?!?!': 'aufgebracht',
               'Who turned off the light!?!': 'aufgebracht',
               'Who turned off the light!?!?!': 'aufgebracht',
               'Was it you?': 'fragend',
               'Is this real life????': 'fragend',
               'Or is this fantasy...': 'fragend',
               'caught in a landslide': 'neutral',
               'and now, the weather': 'neutral'
               }
    for (text, expected) in battery.items():
        actual = soundGenerator.get_mood(text)
        assert actual == expected, (actual, expected)

all_tests.append(test_mood_detection)


# Do we detect the correct source files, and deduce the correct destination files?
# ("source" and "destination" in the context of sound generation / conversion.)
def test_sound_pairing():
    # For each entry e of the test battery it holds that the source-resolution
    # will succeed/fail in exactly the same way on both the minimal sounds
    # environment *and* in the production (heavy) environment.
    # We definitely have:
    # - amsel-neutral.mp3
    # - zilpzalp-fragend-r.mp3
    # - zilpzalp-neutral-r.mp3
    # We definitely do not have:
    # - amsel-fragend.mp3
    # - zilpzalp-aufgebracht-r.mp3
    # - invalid*.mp3
    # However, you should sometimes run this test against 'heavy'.
    battery = [# Positive examples:
               ('amsel', 'neutral', False, 'amsel-neutral'),
               ('zilpzalp', 'fragend', True, 'zilpzalp-fragend-r'),
               ('zilpzalp', 'neutral', True, 'zilpzalp-neutral-r'),
               # Negative examples, ignore mood:
               ('amsel', 'fragend', False, 'amsel-neutral'),
               ('zilpzalp', 'aufgebracht', True, 'zilpzalp-neutral-r'),
               # Negative examples, ignore all:
               ('invalid', 'neutral', False, 'amsel-neutral'),
               ('invalid', 'aufgebracht', True, 'amsel-neutral')]
    mylog.info("You can safely ignore the following warnings about missing files,")
    mylog.info("  because that's exactly what this test is checking.")
    sounds = soundGenerator.SOUND_ROOT
    for (b, m, r, expect_body) in battery:
        actual_source, actual_dest = soundGenerator.find_pair(b, m, r, 6001)
        expect_source = os.path.join(sounds, expect_body + ".mp3")
        expect_dest = os.path.join(sounds, 'processed', expect_body + "-6001.mp3")
        assert actual_source == expect_source, (actual_source, expect_source)
        assert actual_dest == expect_dest, (actual_dest, expect_dest)
        mylog.info("Done.  Warnings about missing files after this are bad.")

all_tests.append(test_sound_pairing)


# Essentially an integration test.
# Given a tweet, do we write the correct thing(s) to the mesage queues?
def test_twitter_listener():
    politicianBackend.check_writeback()
    politicianBackend.set_skip_writeback(True)
    politicianBackend.check_writeback()
    birdBack = birdBackend.BirdBackend()
    polBack = politicianBackend.PoliticianBackend()
    follow = ["4718199753", "813286", "774336282101178368"]
    queue = mq.PrintQueue("twitter_lis_test")
    mylog.info("Preparing for integration test ...")

    fakeTwitter = twitter.FakeTwitterInterface()
    twi = twitterConnection.TwitterConnection(queue, follow, polBack, birdBack, fakeTwitter)
    queue.expect([])
    twi.addCitizen("Heinz1", "zilpzalp", tid="987654")
    # This should be the last test, so don't care about the
    # timer and/or removal of this citizen.
    assert twi.citizens.keys() == {'987654'}
    sounds = soundGenerator.SOUND_ROOT

    mylog.info("Testing reactions to various tweets ...")

    fakeTwitter.send({'content': 'content1',
                      'profile_img': 'img_url',
                      'userscreen': 'userscreen',
                      'hashtags': ['NiceExample', 'TotallyRealistic'],
                      'username': 'HouseOfTweets',
                      'time': '1473446404525',
                      'uid': 4718199753, 'tweet_id': 'bullshit',
                      'retweet': False})
    expect_amsel = os.path.join(sounds, 'processed', 'amsel-neutral-10000.mp3')
    queue.expect([{'poli': 'hot', 'content': 'content1',
                   'hashtags': ['NiceExample', 'TotallyRealistic'],
                   'id': 42, 'image': 'img_url', 'name': 'userscreen', 'partycolor': '#00cc00', 'party': 'Grün',
                   # No 'refresh'
                   'retweet': False, 'sound':
                   {
                     'duration': 10000,
                     'citizen': {'natural': expect_amsel, 'bid': 'amsel'},
                     'poli': {'natural': expect_amsel, 'bid': 'amsel'},
                   },
                   'time': '1473446404525', 'twitterName': 'HouseOfTweets'
                   }])
    fakeTwitter.expect([])

    fakeTwitter.send({'content': 'guy who writes long(?) tweets says whaaaat?',
                      'profile_img': 'img_url',
                      'userscreen': 'Heinzi',
                      'hashtags': [],
                      'username': 'Yoyo',
                      'time': '1473446404527',
                      'uid': 987654, 'tweet_id': 'bullshit',
                      'retweet': True})
    expect_zz = os.path.join(sounds, 'processed', 'zilpzalp-fragend-r-10750.mp3')
    queue.expect([{'poli': None, 'content': 'guy who writes long(?) tweets says whaaaat?',
                   'hashtags': [],
                   'id': 43, 'image': 'img_url', 'name': 'Heinzi', 'partycolor': '#257E9C',  # No 'party'
                   # No 'refresh'
                   'retweet': True, 'sound':
                   {
                     'duration': 10750,
                     'citizen': {'natural': expect_zz, 'bid': 'zilpzalp'},
                     'poli': None,
                   },
                   'time': '1473446404527', 'twitterName': 'Yoyo'
                   }])
    fakeTwitter.expect([])

    fakeTwitter.send({'content': 'Strayer McStray',
                      'profile_img': 'img_url',
                      'userscreen': 'Strayson',
                      'hashtags': [],
                      'username': 'Straynger',
                      'time': '1473446404529',
                      'uid': 5550800911, 'tweet_id': 'bullshit',
                      'retweet': False})
    queue.expect([])
    fakeTwitter.expect([])

    # Put into some known state
    polBack.setBird('648', 'amsel', 'c')
    polBack.setBird('648', 'invalid', 'p')
    assert responseBuilder.NEXT_ACK == 0, 'You inserted/removed a test without updating this one'
    assert ('Ihre Vogelstimme wurde geändert: {fromm} → {to}', 'https://t.co/2FCr67spc6') \
        == (responseBuilder.ACK_TEMPLATES[0], responseBuilder.ACK_LINK), \
        'You changed responseBuilder.py without updating tests.py'
    expect_response = \
        '@RealBarackObama: Ihre Vogelstimme wurde geändert: Goldammer → Amsel https://t.co/2FCr67spc6 #HouseOfTweets'
    # Test receiving a command:
    fakeTwitter.send({'content': 'such an #amsel #HoT',
                      'profile_img': 'img_url',
                      'userscreen': 'The Barack',
                      'hashtags': ['amsel', 'HoT'],
                      'username': 'RealBarackObama',
                      'time': '1473446404527',
                      'uid': 813286, 'tweet_id': 'bullshit',
                      'retweet': False})
    queue.expect([{'poli': '648', 'content': 'such an #amsel #HoT',
                   'hashtags': ['amsel', 'HoT'],
                   'id': 44, 'image': 'img_url', 'name': 'The Barack', 'partycolor': '#429EE2', 'party': 'Demokraten',
                   'refresh': {
                       'politicianId': '648',
                       'birdId': 'amsel',  # Must be the new bird
                   },
                   'retweet': False, 'sound':
                   {
                     'duration': 10000,
                     'citizen': {'natural': expect_amsel, 'bid': 'amsel'},
                     'poli': {'natural': expect_amsel, 'bid': 'amsel'},
                   },
                   'time': '1473446404527', 'twitterName': 'RealBarackObama'
                   }])
    fakeTwitter.expect([('bullshit', expect_response)])

    # FIXME: Test negative replies!

all_tests.append(test_twitter_listener)


def test_all():
    # This might show weird behavior if you modify MANUAL_TESTS by hand
    mylog.info('[TEST] -- Running all tests --')
    for t in all_tests:
        mylog.info("[TEST] {}".format(t))
        t()
        mylog.info("[DONE] {}".format(t))
    mylog.info('[DONE] -- Done with all tests --')


if __name__ == '__main__':
    line = "=" * 80
    mylog.info(line)
    mylog.info("USING REAL TWITTER API!")
    mylog.info("Slow tests = {slow}".format(slow=RUN_SLOW_TESTS))
    mylog.info(line)
    test_all()
