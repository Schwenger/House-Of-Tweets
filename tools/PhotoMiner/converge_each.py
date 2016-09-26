#!/usr/bin/env python3

import json

recently_renamed = {
    # 'Name in poli.json': 'Crawled Name'
}

recently_ejected = {
    'Eva Musterfrau',
}

PROBABLY_NO_TWITTER = {
    'Albert Rupprecht',
    'Albert Stegemann',
    'Alexander Dobrindt',
    'Alexander Hoffmann',
    'Alexander Ulrich',
    'Alexandra Dinges-Dierig',
    'Alois Gerig',
    'Alois Rainer',
    'Andrea Nahles',
    'André Berghegger',
    'Anette Hübinger',
    'Anita Schäfer',
    'Ansgar Heveling',
    'Antje Lezius',
    'Antje Tillmann',
    'Arnold Vaatz',
    'Artur Auernhammer',
    'Astrid Grotelüschen',
    'Azize Tank',
    'Barbara Hendricks',
    'Barbara Lanzinger',
    'Barbara Woltmann',
    'Bartholomäus Kalb',
    'Bernd Rützel',
    'Bernd Westphal',
    'Bernhard Daldrup',
    'Bernhard Schulte-Drüggelte',
    'Bettina Hagedorn',
    'Birgit Kömpel',
    'Birgit Menz',
    'Cajus Caesar',
    'Caren Marks',
    'Carola Stauche',
    'Carsten Körber',
    'Carsten Müller',
    'Carsten Träger',
    'Cemile Giousouf',
    'Christel Voßbeck-Kayser',
    'Christian Haase',
    'Christian Schmidt',
    'Christina Jantz-Herrmann',
    'Christine Lambrecht',
    'Claudia Lücking-Michel',
    'Claudia Tausend',
    'Clemens Binninger',
    'Dagmar Freitag',
    'Daniela Ludwig',
    'Detlef Müller',
    'Dieter Stier',
    'Dietmar Nietan',
    'Dietrich Monstadt',
    'Dirk Fischer',
    'Dirk Vöpel',
    'Dirk Wiese',
    'Doris Barnett',
    'Dorothee Schlegel',
    'Eberhard Gienger',
    'Eckhard Pols',
    'Edelgard Bulmahn',
    'Elfi Scho-Antwerpes',
    'Elisabeth Motschmann',
    'Elisabeth Scharfenberg',
    'Elisabeth Winkelmeier-Becker',
    'Elvira Drobinski-Weiß',
    'Enak Ferlemann',
    'Erich Irlstorfer',
    'Eva Bulling-Schröter',
    'Ewald Schurer',
    'Frithjof Schmidt',
    'Fritz Felgentreu',
    'Gabriele Fograscher',
    'Gabriele Groneberg',
    'Gabriele Schmidt',
    'Georg Kippels',
    'Gerda Hasselfeldt',
    'Gero Storjohann',
    'Gitta Connemann',
    'Günter Baumann',
    'Günter Lach',
    'Gunther Krichbaum',
    'Hans-Georg von der Marwitz',
    'Hans Michelbach',
    'Hans-Peter Uhl',
    'Hans-Ulrich Krüger',
    'Hans-Werner Kammer',
    'Heidrun Bluhm',
    'Heidtrud Henn',
    'Heike Baehrens',
    'Heinrich Zertik',
    'Heinz-Joachim Barchmann',
    'Heinz Riesenhuber',
    'Heinz Wiese',
    'Helga Kühn-Mengel',
    'Helmut Brandt',
    'Helmut Heiderich',
    'Henning Otte',
    'Hermann Färber',
    'Hubert Hüppe',
    'Hubertus Zdebel',
    'Ingo Gädechens',
    'Ingrid Arndt-Brauer',
    'Ingrid Fischbach',
    'Ingrid Pahlmann',
    'Iris Eberl',
    'Iris Gleicke',
    'Joachim Poß',
    'Johannes Fechner',
    'Johannes Röring',
    'Johannes Selle',
    'Johann Saathoff',
    'Jörg Hellmuth',
    'Jutta Eckenbach',
    'Kai Whittaker',
    'Karin Maag',
    'Karin Strenz',
    'Karin Thissen',
    'Karl-Heinz Brunner',
    'Karl Holmeier',
    'Karl Schiewerling',
    'Kathrin Rösel',
    'Katja Keul',
    'Katja Mast',
    'Katrin Kunert',
    'Kees de Vries',
    'Kersten Steinke',
    'Kerstin Kassner',
    'Kerstin Radomski',
    'Kirsten Lühmann',
    'Klaus Barthel',
    'Klaus Brähmig',
    'Klaus-Dieter Gröhler',
    'Klaus Mindrup',
    'Klaus-Peter Flosbach',
    'Klaus-Peter Schulze',
    'Klaus-Peter Willsch',
    'Kordula Kovac',
    'Lothar Riebsamen',
    'Manfred Zöllmer',
    'Margaret Horb',
    'Maria Michalk',
    'Marianne Schieder',
    'Marie-Luise Dött',
    'Marina Kermer',
    'Mark Helfrich',
    'Markus Grübel',
    'Markus Koob',
    'Martina Stamm-Fibich',
    'Martin Dörmann',
    'Martin Gerster',
    'Martin Patzelt',
    'Mathias Middelberg',
    'Matthäus Strebl',
    'Matthias Lietz',
    'Matthias Miersch',
    'Matthias Schmidt',
    'Max Straubinger',
    'Michaela Noll',
    'Michael Brand',
    'Michael Frieser',
    'Michael Gerdes',
    'Michael Hennrich',
    'Michael Stübgen',
    'Michael Vietz',
    'Monika Grütters',
    'Nina Scheer',
    'Norbert Lammert',
    'Norbert Röttgen',
    'Norbert Spinrath',
    'Oliver Grundmann',
    'Oliver Wittke',
    'Oswin Veith',
    'Paul Lehrieder',
    'Peter Bleser',
    'Peter Hintze',
    'Peter Stein',
    'Peter Wichtel',
    'Petra Rode-Bosse',
    'Philipp Murmann',
    'Rainer Spiering',
    'Ralf Brauksiepe',
    'Ralf Kapschack',
    'Ralph Lenkert',
    'Reiner Meier',
    'Reinhard Brandl',
    'Richard Pitterle',
    'Rita Hagl-Kehl',
    'Rita Stockhofe',
    'Robert Hochbaum',
    'Roland Claus',
    'Rolf Mützenich',
    'Rüdiger Veit',
    'Sabine Zimmermann',
    'Siegmund Ehrmann',
    'Sigrid Hupach',
    'Silke Launert',
    'Simone Raatz',
    'Sonja Steffen',
    'Stephan Stracke',
    'Svenja Stadler',
    'Thomas Gambke',
    'Thomas Jurk',
    'Thomas Mahlberg',
    'Thomas Rachel',
    'Thomas Silberhorn',
    'Thomas Viesehon',
    'Thorsten Frei',
    'Uda Heller',
    'Uli Grötsch',
    'Ulla Schmidt',
    'Ulrich Hampel',
    'Ulrich Lange',
    'Ulrike Bahr',
    'Ute Bertram',
    'Ute Finckh-Krämer',
    'Uwe Beckmeyer',
    'Uwe Lagosky',
    'Volker Kauder',
    'Volker Mosblech',
    'Volkmar Vogel',
    'Waldemar Westermayer',
    'Wilfried Lorenz',
    'Willi Brase',
    'Wolfgang Bosbach',
    'Wolfgang Gunkel',
}

KNOWN_NO_TWITTER = {
    'Petra Crone',
    'Sabine Dittmar',
    'Stephan Albani',
    'Norbert Brackmann',
    'Sybille Benning',
    'Katharina Landgraf',
    'Ursula Groden-Kranich',
    'Norbert Schindler',
    'Christoph Bergner',
    'Fritz Güntzler',
    'André Hahn',  # Too many candidates!
    'Birgit Wöllert',
    'Sabine Poschmann',
    'Pia Zimmermann',  # too many!
    'Norbert Barthle',
    'Peter Ramsauer',
    'Wolfgang Schäuble',  # @WolfgaSchaeuble looks like the real one, but it's inactive anyway.
    'Michelle Müntefering',  # @M_Muentefering, but blocked tweets
    'Rudolf Henke',
    'Ulrich Petzold',  # No tweets since 2013
    'Ole Schröder',
    'Lena Strothmann',
    'Burkhard Blienert',
    'Jeannine Pflugradt',  # Too many similar ones, no exact
    'Andreas Jung',  # Too many
    'Emmi Zeulner',
    'Thomas Stritzl',
    'Martin Pätzold',  # Too many
    'Patricia Lips',  # What the
    'Sylvia Jörrißen',
    'Sascha Raabe',
    'Gernot Erler',  # Curiously, taken by a Russian.
    'Michael Donth',
    'Maria Flachsbarth',
    'Thomas de Maizière',  # Aww
    'Dirk Heidenblut',
    'Iris Ripsam',  # Unsurprisingly
    'Gülistan Yüksel',  # Wow that's many!
    'Axel Knoerig',
    'Ursula Schulte',
    'Frank-Walter Steinmeier',  # Aww
    'Karl A. Lamers',
    'Josef Rief',
    'Sarah Ryglewski',
    'Axel Schäfer',
    'Sabine Weiss',  # Way too many
    'Angela Merkel',  # Aww. 'AngelaMerkeICDU' -- with a capital 'i' not a lower-case 'L'.  I'm wary.
    'Stephan Mayer',  # Oh god
    'Josef Göppel',  # Empty account
    'Detlef Seif',  # Empty account
    'Carola Reimann',  # Two empty accounts (?)
    'Astrid Timmermann-Fechter',
    'Veronika Bellmann',
    'Alois Karl',
    'Daniela De Ridder',  # Full setup,  but no tweets
    'Carsten Linnemann',
    'Karin Evers-Meyer',
    'Reinhold Sendker',
    'Sabine Sütterlin-Waack',
    'Albert Weiler',
    'Andreas G. Lämmel',
    'Philipp Graf Lerchenfeld',  # Aww
    'Hans-Joachim Schabedoth',
    'Thomas Dörflinger',
    'Alexander Funk',
    'Ulrike Gottschalck',
    'Gabriele Lösekrug-Möller',
    'Hendrik Hoppenstedt',  # Früher war mehr Lametta!
    'Gustav Herzog',
    'Karl-Heinz Helmut Wange',
    'Bernhard Kaster',
}

# NOTE: silent assumption: name==full_name for these entries!
recently_joined = {
    # 'Max Mustermann': {
    #     "self_bird": "gimpel",
    #     "cv": {
    #         "en": "Max Mustermann is a German politician. He/She/FIXME is a member of the FIXME.",
    #         "de": "FIXME"
    #     },
    #     "citizen_bird": "star"
    #     "twittering": {"twitterUserName": "MusterMax"}
    # },
}

twitter_stats = {'poli': 0, 'both': 0}

spoof_images = {
    'Helmut Nowak': {
        "copyright": "Helmut Nowak / Jutta Hartmann",
        "license": "unknown-bundestag",
        "url": "https://www.bundestag.de/image/242050/Hochformat__2x3/177/265/399f0e3ef04b5cae4f0eb804f3dbee72/sy/nowak_helmut_fedor_gross.jpg"
    },
    'Heiko Schmelzle': {
        "copyright": "Heiko Schmelzle / Martinus Ekkenga",
        "license": "unknown-bundestag",
        "url": "https://www.bundestag.de/image/241662/Hochformat__2x3/177/265/d596b81b20c8069cc73e47d21e38971d/fz/schmelzle_heiko_gross.jpg"
    },
}


def merge_handle(old_twittering, new_handle):
    # Set of known-outdated Twitter-accounts:
    twitter_outdated = {
        'peternachberlin',
        'GabiKatzmarek',
        'bernhardkaster',
    }
    if new_handle in twitter_outdated:
        new_handle = None
    assert old_twittering is not None

    # Actual logic:
    if new_handle is None:
        twitter_stats['poli'] += 1
        return old_twittering
    else:
        twitter_stats['both'] += 1
        # false positive
        # noinspection PyUnresolvedReferences
        old_handle = old_twittering['twitterUserName']
        assert old_handle.lower() == new_handle.lower(), (old_handle, new_handle)
        return old_twittering


def merge_single(agg, poli):
    if 'party' in poli:
        assert poli['party'] == agg['party'], (poli['party'], agg['party'])

    new_poli = dict()
    for key in ['name', 'full_name', 'imgs', 'party']:
        new_poli[key] = agg[key]
    for key in ['self_bird', 'pid', 'cv', 'citizen_bird']:
        new_poli[key] = poli[key]

    twit = merge_handle(poli.get('twittering'), agg.get('twitter_handle'))
    if twit is not None:
        new_poli['twittering'] = twit
    else:
        print('[WARN] No twitter found for MdB ' + agg['full_name'])

    # Discard agg['srcs']
    return new_poli


def merge_all(by_name, padded_polis):
    all_merged = []
    spurious_poli = []

    for poli in padded_polis:
        assert 'twittering' in poli
        name = poli['name']
        if name in recently_renamed:
            name = recently_renamed[name]
        if name in recently_ejected or name == 'House Of Tweets':
            # "House Of Tweets" will be injected back later on,
            # but for now it's in the way.
            continue
        agg = by_name.get(name)
        if agg is None:
            print('Spurious poli: ' + poli['name'])
            spurious_poli.append(poli)
            # Error!  But don't throw right away, as the overview might be helpful
            # in finding out whether it's "just" a rename, or maybe someone got ejected.
            continue
        del by_name[name]
        all_merged.append(merge_single(agg, poli))

    by_name = {k: v for k, v in by_name.items()
               if v['name'] not in PROBABLY_NO_TWITTER and v['name'] not in KNOWN_NO_TWITTER}
    # Check whether merging worked fine
    assert len(by_name) == 0 and len(spurious_poli) == 0,\
        "unexpectedly unmatched: agg={}, poli={}".format(by_name, spurious_poli)

    # All "new" entries were already spoofed into the polis list.

    return all_merged


def load_by_name():
    with open('wikify_each.json', 'r') as fp:
        # TODO: In later versions, don't use 'name' but rather 'full_name'
        by_name = {e['name']: e for e in json.load(fp)}
    for name, img in spoof_images.items():
        poli = by_name[name]
        imgs = poli['imgs']
        assert len(imgs) == 0
        imgs['spoofed'] = img
    return by_name


def load_padded_polis():
    with open('../../backend/pols.json', 'r') as fp:
        polis = json.load(fp).values()
    polis = list(sorted(polis, key=lambda x: x['pid']))

    max_pid = 1
    for poli in polis:
        try:
            # (false positive)
            # noinspection PyTypeChecker
            this_pid = int(poli['pid'])
        except ValueError:
            # Ignore non-numeric pids
            continue
        max_pid = max(max_pid, this_pid)

    for name, j in sorted(recently_joined.items(), key=lambda x: x[0]):
        j['name'] = name
        max_pid += 1
        j['pid'] = str(max_pid)
        polis.append(j)

    return polis


def run():
    by_name = load_by_name()
    polis = load_padded_polis()
    merged = merge_all(by_name, polis)
    print('Merge stats:')
    for k, v in twitter_stats.items():
        print('    {}: {}'.format(k, v))
    print('    agg: {}'.format(len(recently_joined)))
    print('    neither: {}'.format(len(KNOWN_NO_TWITTER) + len(PROBABLY_NO_TWITTER)))
    with open('converge_each.json', 'w') as fp:
        json.dump(merged, fp, sort_keys=True, indent=2)


if __name__ == '__main__':
    run()
