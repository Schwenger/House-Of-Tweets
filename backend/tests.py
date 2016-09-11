#!/usr/bin/env python3

import json
import mq
import twitter
import twitterConnection
import birdBackend
import politicianBackend
import soundGenerator

all_tests = []
MANUAL_TESTS = False
REAL_TWITTER_TESTS = False


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
                'userscreen': 'HouseOfTweetsSB',
                'hashtags': ['Improved', 'Harder', 'Faster', 'Stronger'],
                'username': 'HouseOfTweets',
                'time': '1473446404525',
                'uid': '4718199753',
                'retweet': True}
    assert actual == expected

all_tests.append(test_parse_tweet)


def test_name_resolution():
    if not REAL_TWITTER_TESTS:
        print("[SKIP] Not allowed to contact real Twitter")
        return
    ids = {'HouseOfTweetsSB': '4718199753',
           '@HouseOfTweetsSB': '4718199753',
           '@MissesVlog': '50712079',
           'eeQu0Ae4': '774336282101178368',
           'SarcasticTester': '720224609560371201',
           'HopefullyNotARealTwitterAccount': None}
    twi = twitter.RealTwitterInterface()
    for (user, expect_id) in ids.items():
        actual_id = twi.resolve_name(user)
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
    print("[MANU] Please check by hand whether this generates the file on the\n"
          "       first call and uses the cached version on the second:")
    actual = soundGenerator.generate_sound('Cheerio, buddy', False, 'amsel', 'amsel')
    print("[MANU] (end)")
    path_amsel = os.path.join(soundGenerator.SOUND_ROOT, 'processed/amsel-neutral-6000.mp3')
    desc_amsel = {'natural': path_amsel, 'synth': path_amsel}
    expected = {'duration': 6000, 'citizen': desc_amsel, 'poli': desc_amsel}
    assert actual == expected, (actual, expected)

    content = "How can mirrors be real if our eyes aren't real?"
    actual = soundGenerator.generate_sound(content, True, 'zilpzalp', None)
    path_zz = os.path.join(soundGenerator.SOUND_ROOT, 'processed/zilpzalp-fragend-r-12000.mp3')
    desc_zz = {'natural': path_zz, 'synth': path_zz}
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
    print("You can safely ignore the following warnings about missing files,")
    print("  because that's exactly what this test is checking.")
    sounds = soundGenerator.SOUND_ROOT
    for (b, m, r, expect_body) in battery:
        actual_source, actual_dest = soundGenerator.find_pair(b, m, r, 6001)
        expect_source = os.path.join(sounds, expect_body + ".mp3")
        expect_dest = os.path.join(sounds, 'processed', expect_body + "-6001.mp3")
        assert actual_source == expect_source, (actual_source, expect_source)
        assert actual_dest == expect_dest, (actual_dest, expect_dest)
    print("Done.  Warnings about missing files after this are bad.")

all_tests.append(test_sound_pairing)


def test_twitter_listener():
    politicianBackend.check_writeback()
    politicianBackend.set_skip_writeback(True)
    politicianBackend.check_writeback()
    birdBack = birdBackend.BirdBackend()
    polBack = politicianBackend.PoliticianBackend()
    follow = ["4718199753", "774336282101178368"]
    queue = mq.PrintQueue("twitter_lis_test")
    print("[INFO] Preparing for integration test …")

    fakeTwitter = twitter.FakeTwitterInterface()
    twi = twitterConnection.TwitterConnection(queue, follow, polBack, birdBack, fakeTwitter)
    queue.expect([])
    twi.addCitizen("Heinz1", "zilpzalp", tid="987654")
    assert twi.citizens.keys() == {'987654'}
    sounds = soundGenerator.SOUND_ROOT

    print("[INFO] Testing reactions to various tweets …")

    fakeTwitter.send({'content': 'content1',
                      'profile_img': 'img_url',
                      'userscreen': 'userscreen',
                      'hashtags': ['NiceExample', 'TotallyRealistic'],
                      'username': 'HouseOfTweets',
                      'time': '1473446404525',
                      'uid': 4718199753,
                      'retweet': False})
    expect_amsel = sounds + '/processed/amsel-neutral-6000.mp3'
    queue.expect([{'byPoli': True, 'content': 'content1',
                   'hashtags': ['NiceExample', 'TotallyRealistic'],
                   'id': 42, 'image': 'img_url', 'name': 'userscreen', 'partycolor': '#00cc00',
                   # No 'refresh'
                   'retweet': False, 'sound':
                   {
                     'duration': 6000,
                     'citizen': {'natural': expect_amsel, 'synth': expect_amsel},
                     'poli': {'natural': expect_amsel, 'synth': expect_amsel},
                   },
                   'time': '1473446404525', 'twitterName': 'HouseOfTweets'
                   }])

    fakeTwitter.send({'content': 'guy who writes long(?) tweets says what?',
                      'profile_img': 'img_url',
                      'userscreen': 'Heinzi',
                      'hashtags': [],
                      'username': 'Yoyo',
                      'time': '1473446404527',
                      'uid': 987654,
                      'retweet': True})
    expect_zz = sounds + '/processed/zilpzalp-fragend-r-10000.mp3'
    queue.expect([{'byPoli': False, 'content': 'guy who writes long(?) tweets says what?',
                   'hashtags': [],
                   'id': 43, 'image': 'img_url', 'name': 'Heinzi', 'partycolor': '#257E9C',
                   # No 'refresh'
                   'retweet': True, 'sound':
                   {
                     'duration': 10000,
                     'citizen': {'natural': expect_zz, 'synth': expect_zz},
                     'poli': None,
                   },
                   'time': '1473446404527', 'twitterName': 'Yoyo'
                   }])

    fakeTwitter.send({'content': 'Strayer McStray',
                      'profile_img': 'img_url',
                      'userscreen': 'Strayson',
                      'hashtags': [],
                      'username': 'Straynger',
                      'time': '1473446404529',
                      'uid': 5550800911,
                      'retweet': False})
    queue.expect([])

    # TODO: Test for updates of a politician's bird?

all_tests.append(test_twitter_listener)


def test_poli_writeback():
    print("Testing politicianBackend.setBird.  I hope you saved your stuff!")
    politicianBackend.check_writeback()
    politicianBackend.set_skip_writeback(False)
    politicianBackend.check_writeback()
    print("Running against Armin Schuster (395912134)")
    print("original self_bird: weisskopfseeadler")
    print("original citizen_bird: fitis")
    pB = politicianBackend.PoliticianBackend()
    #pB.setBird('395912134', 'ara', 'p')
    #pB.setBird('395912134', 'mauersegler', 'c')
    pB.setBird('395912134', 'fitis', 'c')
    print("Now check by hand.")
    raise AssertionError("Can't continue after this point.")

# Don't automatically run the above test!


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
    line = "=" * 80
    import os.path
    if os.path.isfile('credentials.py'):
        print(line + "\nUSING REAL TWITTER API!\n" + line)
        REAL_TWITTER_TESTS = True
    else:
        print(line + "\nNo credentials.py found!  Won't connect to Twitter.")
        if not MANUAL_TESTS:
            print("Enabling MANUAL_TESTS, to check RabbitMQ connectivity")
            MANUAL_TESTS = True
        print(line)

    test_all()
