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

# NOTE: silent assumption: name==full_name for these entries!
allow_spurious_poli = {
    'Barack Obama',
    'François Hollande',
    'House Of Tweets',
}


def merge(agg, poli):
    if poli.get('images') is not None:
        # This fails currently.
        assert len(agg['imgs']) > 0, (agg, poli)
    # FIXME
    return {'agg': agg, 'poli': poli, 'full_name': agg['full_name']}


def merge_pseudo(name, poli):
    # FIXME
    return {'poli': poli, 'full_name': name}


def merge_all(by_name, padded_polis):
    all_merged = []
    spurious_poli = []

    for poli in padded_polis:
        name = poli['name']
        if name in recently_renamed:
            name = recently_renamed[name]
        if name in recently_ejected:
            continue
        if name in allow_spurious_poli:
            all_merged.append(merge_pseudo(name, poli))
            continue
        agg = by_name.get(name)
        if agg is None:
            spurious_poli.append(poli)
            # Error!  But don't throw right away, as the overview might be helpful
            # in finding out whether it's "just" a rename, or maybe someone got ejected.
            continue
        del by_name[name]
        all_merged.append(merge(agg, poli))
    assert len(by_name) == 0, "unmatched: agg={}, poli={}".format(by_name, spurious_poli)

    return all_merged


def load_agg_by_name():
    with open('aggregate-each.json', 'r') as fp:
        # TODO: In later versions, don't use 'name' but rather 'full_name'
        return {e['name']: e for e in json.load(fp)}
        # if e['name'] not in recently_ejected}  # TODO: Necessary?


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

    for name, j in recently_joined.items():
        j['name'] = name
        max_pid += 1
        j['pid'] = max_pid
        polis.append(j)

    return polis


def run():
    by_name = load_agg_by_name()
    polis = load_padded_polis()
    merged = merge_all(by_name, polis)
    # FIXME: Sort before writing!
    with open('fill-in.json', 'w') as fp:
        json.dump(merged, fp, sort_keys=True, indent=2)


if __name__ == '__main__':
    run()
