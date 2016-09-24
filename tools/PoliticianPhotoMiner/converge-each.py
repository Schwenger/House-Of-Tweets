#!/usr/bin/env python3

import json

recently_renamed = {
    # 'Name in poli.json': 'Crawled Name'
    'Alexander Neu': 'Alexander S. Neu',
    'Alois Georg Josef Rainer': 'Alois Rainer',
    'Andreas Lämmel': 'Andreas G. Lämmel',
    'Axel Fischer': 'Axel E. Fischer',
    'Cajus Julius Caesar': 'Cajus Caesar',
    'Christian von Stetten': 'Christian Freiherr von Stetten',
    'Christina Jantz': 'Christina Jantz-Herrmann',
    'Dagmar Wöhrl': 'Dagmar G. Wöhrl',
    'Elisabeth Charlotte Motschmann': 'Elisabeth Motschmann',
    'Elisabeth Paus': 'Lisa Paus',
    'Johann Wadephul': 'Johann David Wadephul',
    'Mark André Helfrich': 'Mark Helfrich',
    'Matthias Birkwald': 'Matthias W. Birkwald',
    'Michaela Engelmeier-Heite': 'Michaela Engelmeier',
    'Patrick Ernst Sensburg': 'Patrick Sensburg',
    'Philipp Graf von und zu Lerchenfeld': 'Philipp Graf Lerchenfeld',
    'Pia-Beate Zimmermann': 'Pia Zimmermann',
    'Ursula Schauws': 'Ulle Schauws',
    'Volker Michael Ullrich': 'Volker Ullrich',
}

recently_ejected = {
    'Andreas Schockenhoff',
    'Annette Schavan',
    'Carsten Sieling',
    'Christina Kampmann',
    'Diana Golze',
    'Dirk Becker',
    'Hans-Peter Bartels',
    'Katherina Reiche',
    'Peter Gauweiler',
    'Peter Hinz',
    'Petra Hinz',
    'Philipp Mißfelder',
    'Priska Hinz',
    'Reinhard Grindel',
    'Reinhold Jost',
    'Ronald Pofalla',
    'Sabine Bätzing-Lichtenthäler',
    'Sebastian Edathy',
    'Steffen Kampeter',
    'Thomas Strobl',
    'Wolfgang Tiefensee',
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
    'Iris Ripsam': {
        "self_bird": "goldammer",
        "cv": {
            "en": "Iris Ripsam is a German politician. She is a member of the CDU.",
            # There is no Wikipedia entry, sorry.
            "de": "Iris Ripsam ist eine deutsche Politikerin. Sie ist Mitglied der CDU."
        },
        "citizen_bird": "fitis"
    },
    'Jürgen Coße': {
        "self_bird": "rauchschwalbe",
        "cv": {
            "en": "Jürgen Coße is a German politician. He is a member of the SPD.",
            # Manually adapted.
            "de": "Jürgen Coße (* 16. August 1969) ist ein deutscher Politiker (SPD)."
                  " Er ist seit 1986 Mitglied der SPD. Dort ist er Vorsitzender des Unterbezirkes"
                  " Steinfurt und gehört zurzeit dem Ortsverein Neuenkirchen an."
        },
        "citizen_bird": "rotkehlchen"
    },
    'Karl-Heinz Helmut Wange': {
        "self_bird": "tukan",
        "cv": {
            "en": "Karl-Heinz Helmut Wange is a German politician. He is a member of the CDU.",
            # There is no Wikipedia entry, sorry.
            "de": "Karl-Heinz Helmut Wange ist ein deutscher Politiker. Er ist Mitglied der CDU."
        },
        "citizen_bird": "mehlschwalbe"
    },
    'Kathrin Rösel': {
        "self_bird": "dohle",
        "cv": {
            "en": "Kathrin Rösel is a German politician. She is a member of the CDU.",
            "de": "Kathrin Rösel (* 4. November 1970 in Stendal) ist eine deutsche Politikerin (CDU)."
                  " Seit dem 4. Juni 2016 gehört sie dem 18. Deutschen Bundestag an."
        },
        "citizen_bird": "bachstelze"
    },
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
            spurious_poli.append(poli)
            # Error!  But don't throw right away, as the overview might be helpful
            # in finding out whether it's "just" a rename, or maybe someone got ejected.
            continue
        del by_name[name]
        all_merged.append(merge_single(agg, poli))

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
        polis = json.load(fp)

    max_pid = 1
    for poli in polis:
        try:
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
