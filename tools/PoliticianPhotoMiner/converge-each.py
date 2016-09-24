#!/usr/bin/env python3

import json

recently_renamed = {
    # 'Name in poli.json': 'Crawled Name'
}

recently_ejected = {
    'Eva Musterfrau',
}

# Must also include all politicians that don't appear
# in pols.json due to not having a twitter account.
missing_in_pols = {
    'Albert Rupprecht',
    'Albert Stegemann',
    'Albert Weiler',
    'Alexander Dobrindt',
    'Alexander Funk',
    'Alexander Hoffmann',
    'Alexander Ulrich',
    'Alexandra Dinges-Dierig',
    'Alois Gerig',
    'Alois Karl',
    'Alois Rainer',
    'Andrea Nahles',
    'Andreas G. Lämmel',
    'Andreas Jung',
    'André Berghegger',
    'André Hahn',
    'Anette Hübinger',
    'Angela Merkel',
    'Anita Schäfer',
    'Ansgar Heveling',
    'Antje Lezius',
    'Antje Tillmann',
    'Arnold Vaatz',
    'Artur Auernhammer',
    'Astrid Grotelüschen',
    'Astrid Timmermann-Fechter',
    'Axel Knoerig',
    'Axel Schäfer',
    'Azize Tank',
    'Barbara Hendricks',
    'Barbara Lanzinger',
    'Barbara Woltmann',
    'Bartholomäus Kalb',
    'Bernd Rützel',
    'Bernd Westphal',
    'Bernhard Daldrup',
    'Bernhard Kaster',
    'Bernhard Schulte-Drüggelte',
    'Bettina Hagedorn',
    'Birgit Kömpel',
    'Birgit Menz',
    'Birgit Wöllert',
    'Burkhard Blienert',
    'Cajus Caesar',
    'Caren Marks',
    'Carola Reimann',
    'Carola Stauche',
    'Carsten Körber',
    'Carsten Linnemann',
    'Carsten Müller',
    'Carsten Träger',
    'Cemile Giousouf',
    'Christel Voßbeck-Kayser',
    'Christian Haase',
    'Christian Schmidt',
    'Christina Jantz-Herrmann',
    'Christine Lambrecht',
    'Christoph Bergner',
    'Claudia Lücking-Michel',
    'Claudia Tausend',
    'Clemens Binninger',
    'Dagmar Freitag',
    'Daniela De Ridder',
    'Daniela Ludwig',
    'Detlef Müller',
    'Detlef Seif',
    'Dieter Stier',
    'Dietmar Nietan',
    'Dietrich Monstadt',
    'Dirk Fischer',
    'Dirk Heidenblut',
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
    'Emmi Zeulner',
    'Enak Ferlemann',
    'Erich Irlstorfer',
    'Eva Bulling-Schröter',
    'Ewald Schurer',
    'Frank-Walter Steinmeier',
    'Frithjof Schmidt',
    'Fritz Felgentreu',
    'Fritz Güntzler',
    'Gabriele Fograscher',
    'Gabriele Groneberg',
    'Gabriele Lösekrug-Möller',
    'Gabriele Schmidt',
    'Georg Kippels',
    'Gerda Hasselfeldt',
    'Gernot Erler',
    'Gero Storjohann',
    'Gitta Connemann',
    'Gülistan Yüksel',
    'Günter Baumann',
    'Günter Lach',
    'Gunther Krichbaum',
    'Gustav Herzog',
    'Hans-Georg von der Marwitz',
    'Hans-Joachim Schabedoth',
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
    'Hendrik Hoppenstedt',
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
    'Iris Ripsam',
    'Jeannine Pflugradt',
    'Joachim Poß',
    'Johannes Fechner',
    'Johannes Röring',
    'Johannes Selle',
    'Johann Saathoff',
    'Jörg Hellmuth',
    'Josef Göppel',
    'Josef Rief',
    'Jutta Eckenbach',
    'Kai Whittaker',
    'Karin Evers-Meyer',
    'Karin Maag',
    'Karin Strenz',
    'Karin Thissen',
    'Karl A. Lamers',
    'Karl-Heinz Brunner',
    'Karl-Heinz Helmut Wange',
    'Karl Holmeier',
    'Karl Schiewerling',
    'Katharina Landgraf',
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
    'Lena Strothmann',
    'Lothar Riebsamen',
    'Manfred Zöllmer',
    'Margaret Horb',
    'Maria Flachsbarth',
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
    'Martin Pätzold',
    'Mathias Middelberg',
    'Matthäus Strebl',
    'Matthias Lietz',
    'Matthias Miersch',
    'Matthias Schmidt',
    'Max Straubinger',
    'Michaela Noll',
    'Michael Brand',
    'Michael Donth',
    'Michael Frieser',
    'Michael Gerdes',
    'Michael Hennrich',
    'Michael Stübgen',
    'Michael Vietz',
    'Michelle Müntefering',
    'Monika Grütters',
    'Nina Scheer',
    'Norbert Barthle',
    'Norbert Brackmann',
    'Norbert Lammert',
    'Norbert Röttgen',
    'Norbert Schindler',
    'Norbert Spinrath',
    'Ole Schröder',
    'Oliver Grundmann',
    'Oliver Wittke',
    'Oswin Veith',
    'Patricia Lips',
    'Paul Lehrieder',
    'Peter Bleser',
    'Peter Hintze',
    'Peter Ramsauer',
    'Peter Stein',
    'Peter Wichtel',
    'Petra Crone',
    'Petra Rode-Bosse',
    'Philipp Graf Lerchenfeld',
    'Philipp Murmann',
    'Pia Zimmermann',
    'Rainer Spiering',
    'Ralf Brauksiepe',
    'Ralf Kapschack',
    'Ralph Lenkert',
    'Reiner Meier',
    'Reinhard Brandl',
    'Reinhold Sendker',
    'Richard Pitterle',
    'Rita Hagl-Kehl',
    'Rita Stockhofe',
    'Robert Hochbaum',
    'Roland Claus',
    'Rolf Mützenich',
    'Rüdiger Veit',
    'Rudolf Henke',
    'Sabine Dittmar',
    'Sabine Poschmann',
    'Sabine Sütterlin-Waack',
    'Sabine Weiss',
    'Sabine Zimmermann',
    'Sarah Ryglewski',
    'Sascha Raabe',
    'Siegmund Ehrmann',
    'Sigrid Hupach',
    'Silke Launert',
    'Simone Raatz',
    'Sonja Steffen',
    'Stephan Albani',
    'Stephan Mayer',
    'Stephan Stracke',
    'Svenja Stadler',
    'Sybille Benning',
    'Sylvia Jörrißen',
    'Thomas de Maizière',
    'Thomas Dörflinger',
    'Thomas Gambke',
    'Thomas Jurk',
    'Thomas Mahlberg',
    'Thomas Rachel',
    'Thomas Silberhorn',
    'Thomas Stritzl',
    'Thomas Viesehon',
    'Thorsten Frei',
    'Uda Heller',
    'Uli Grötsch',
    'Ulla Schmidt',
    'Ulrich Hampel',
    'Ulrich Lange',
    'Ulrich Petzold',
    'Ulrike Bahr',
    'Ulrike Gottschalck',
    'Ursula Groden-Kranich',
    'Ursula Schulte',
    'Ute Bertram',
    'Ute Finckh-Krämer',
    'Uwe Beckmeyer',
    'Uwe Lagosky',
    'Veronika Bellmann',
    'Volker Kauder',
    'Volker Mosblech',
    'Volkmar Vogel',
    'Waldemar Westermayer',
    'Wilfried Lorenz',
    'Willi Brase',
    'Wolfgang Bosbach',
    'Wolfgang Gunkel',
    'Wolfgang Schäuble',
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
    # },
}

twitter_stats = {'neither': 0, 'poli': 0, 'agg': 0, 'both': 0}


def merge_handle(old_twittering, new_handle):
    # Set of known-outdated Twitter-accounts:
    twitter_outdated = {
        'peternachberlin',
        'GabiKatzmarek',
        'bernhardkaster',
    }
    if new_handle in twitter_outdated:
        new_handle = None
    if old_twittering is not None and old_twittering['twitterUserName'] in twitter_outdated:
        old_twittering = None

    # Actual logic:
    if old_twittering is None:
        if new_handle is None:
            twitter_stats['neither'] += 1
            return None
        else:
            twitter_stats['agg'] += 1
            return {'twitterUserName': new_handle}
    else:
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

    by_name = {k: v for k, v in by_name.items() if v['name'] not in missing_in_pols}
    # Check whether merging worked fine
    assert len(by_name) == 0 and len(spurious_poli) == 0,\
        "unexpectedly unmatched: agg={}, poli={}".format(by_name, spurious_poli)

    # All "new" entries were already spoofed into the polis list.

    return all_merged


def load_by_name():
    with open('wikify-each.json', 'r') as fp:
        # TODO: In later versions, don't use 'name' but rather 'full_name'
        return {e['name']: e for e in json.load(fp)}


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
    # FIXME: Sort before writing!
    with open('converge-each.json', 'w') as fp:
        json.dump(merged, fp, sort_keys=True, indent=2)


if __name__ == '__main__':
    run()
