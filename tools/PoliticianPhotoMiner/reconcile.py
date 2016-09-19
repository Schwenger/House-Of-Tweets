#!/usr/bin/env python3

import json

lookup = dict()

with open('crawl-each.json', 'r') as in_lookup:
    for entry in json.load(in_lookup):
        lookup[entry['page']] = entry['page_file']

with open('parse-roots.json', 'r') as in_data:
    stored_data = json.load(in_data)

for entry in stored_data:
    entry['page_file'] = lookup[entry['page']]

with open('reconciled.json', 'w') as out:
    json.dump(stored_data, out, sort_keys=True, indent=2)
