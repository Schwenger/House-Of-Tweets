#!/usr/bin/env python3

import json

recently_renamed = {
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

recently_joined = {
#    'Max Mustermann': {
#        "self_bird": "gimpel",
#        "cv": {
#            "en": "Max Mustermann is a German politician. He/She/FIXME is a member of the FIXME.",
#            "de": "FIXME"
#        },
#        "citizen_bird": "star"
#    },
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
            "de": "Jürgen Coße (* 16. August 1969) ist ein deutscher Politiker (SPD). Er ist seit 1986 Mitglied der SPD. Dort ist er Vorsitzender des Unterbezirkes Steinfurt und gehört zurzeit dem Ortsverein Neuenkirchen an."
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
            "de": "Kathrin Rösel (* 4. November 1970 in Stendal) ist eine deutsche Politikerin (CDU). Seit dem 4. Juni 2016 gehört sie dem 18. Deutschen Bundestag an."
        },
        "citizen_bird": "bachstelze"
    },
}

allow_spurious_poli = {
    'Barack Obama',
    'François Hollande',
    'House Of Tweets',
}

with open('aggregate-each.json', 'r') as fp:
    aggregated = json.load(fp)

with open('../../backend/pols.json', 'r') as fp:
    old_pols = json.load(fp)

aggregated_by_name = {e['name']: e for e in aggregated}

poli_only = []

for poli in old_pols:
    name = poli['name']
    if name in recently_renamed:
        name = recently_renamed[name]
    e = aggregated_by_name.get(name)
    if name in recently_ejected:
        continue
    if e is None:
        aggregated_by_name[name] = {'seen': True}
        poli_only.append(name)
        continue
    assert 'seen' not in e, 'Second coming of {}'.format(name)
    e['seen'] = True

agg_only = [e['name'] for e in aggregated if 'seen' not in e]

for x in sorted(poli_only):
    print(x + '_poli')
for x in sorted(agg_only):
    print(x + '_agg')

# with open('parse-each.json', 'r') as fp:
#     ejected = [e['full_name'].replace('Prof. ', '').replace('Dr. ', '')
#                              .replace('h. c. ', '').replace('h.c. ', '')
#                for e in json.load(fp) if e.get('ejected')]
# # 
# for x in sorted(ejected):
#     print(x + '_ej')
