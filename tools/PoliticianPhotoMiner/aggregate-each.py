#!/usr/bin/env python3

import json

resolutions = {
    # Fix inconsistent naming:
    'Karl-Heinz (Charles M.) Huber': 'Charles M. Huber',
    'Karl-Heinz Wange': 'Karl-Heinz Helmut Wange',
    'Sevim Dagdelen': 'Sevim Da\u011fdelen',
    'Dr. Alexander Neu': 'Dr. Alexander S. Neu',
    'Andreas L\u00e4mmel': 'Andreas G. L\u00e4mmel',
    'Chris K\u00fchn': 'Christian K\u00fchn',
    'Dr. Johann Wadephul': 'Dr. Johann David Wadephul',
    # Shorten overly-long titles:
    'Prof. Dr. iur. Heribert Hirte': 'Prof. Dr. Heribert Hirte',
    'Dr. rer. nat. Ute Finckh-Kr\u00e4mer': 'Dr. Ute Finckh-Kr\u00e4mer',
    'Dr. rer. pol. Daniela De Ridder': 'Dr. Daniela De Ridder',
    'Dr. Dr. h.c. Karl A. Lamers': 'Dr. Karl A. Lamers',
    'Dr. rer. nat. Karamba Diaby': 'Dr. Karamba Diaby',
    'Dr. med. vet. Wilhelm Priesmeier': 'Dr. Wilhelm Priesmeier',
    'Dr. med. vet. Karin Thissen': 'Dr. Karin Thissen',
    'Dr. iur. Georg N\u00fc\u00dflein': 'Dr. Georg N\u00fc\u00dflein',
    # Really?
    'Dr. Konstantin von\u00a0Notz': 'Dr. Konstantin von Notz',
    # Stick to the longer title, as they might obsess about it:
    'Dr. Egon J\u00fcttner': 'Prof. Dr. Egon J\u00fcttner',
    'Dr. Karl Lauterbach': 'Prof. Dr. Karl Lauterbach',
    'Monika Gr\u00fctters': 'Prof. Monika Gr\u00fctters',
}


def find_name(entries):
    # Hard-codedly extract the field 'name'.
    assert(len(entries) == 2)
    # For higher 'n', there sure is a better way to do it.
    if 'name' in entries[0]:
        bundestag = entries[0]
        party = entries[1]
    elif 'name' in entries[1]:
        bundestag = entries[1]
        party = entries[0]
    else:
        assert False, entries
    assert bundestag['src'] == 'bundestag'
    assert party['src'] != 'bundestag'
    return bundestag['name']


def load_filtered_entries():
    ejected_names = []

    by_full_name = dict()

    with open('parse-each.json', 'r') as fp:
        for entry in json.load(fp):
            full_name = entry['full_name']
            resolved_name = resolutions.get(full_name)
            if resolved_name is not None:
                full_name = resolved_name
            if 'ejected' in entry and entry['ejected']:
                ejected_names.append(full_name)
                continue

            # Actually add:
            if full_name in by_full_name:
                bfn_entry = by_full_name[full_name]
            else:
                bfn_entry = []
                by_full_name[full_name] = bfn_entry
            bfn_entry.append(entry)

    return {k: v for (k, v) in by_full_name.items() if k not in ejected_names}


# Actual aggregation code.
def aggregate(full_name, entries):
    agg_entry = {'full_name': full_name,
                 'name': find_name(entries),
                 'srcs': {e['src']: e['page'] for e in entries},
                 'imgs': {e['src']: e['img'] for e in entries if 'img' in e}
                 }

    # Determine Twitter-Handle
    handles = set()
    for e in entries:
        if 'twitter_handle' not in e:
            continue
        handles.add(e['twitter_handle'])
    assert len(handles) <= 1, handles
    if len(handles) == 1:
        agg_entry['twitter_handle'] = list(handles)[0]

    # Determine the party (hardcoded for len(entries) == 2)
    assert len(entries) == 2, len(entries)
    party_sets = [set(e['possible_parties']) for e in entries]
    assert len(party_sets) == 2, "Dafuq"
    party_inter = party_sets[0].intersection(party_sets[1])
    assert len(party_inter) == 1, (party_inter, entries)
    agg_entry['party'] = list(party_inter)[0]

    return agg_entry


raw_entries = load_filtered_entries()
aggregated = [aggregate(k, v) for (k, v) in raw_entries.items()]

assert len(aggregated) == 630, 'Expected 630 in the Budnestag, but found {}'.format(len(aggregated))

with open('aggregate-each.json', 'w') as fp:
    json.dump(aggregated, fp, sort_keys=True, indent=2)
print('Done.')
