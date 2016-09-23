#!/usr/bin/env python3

import nice
import json

with open('wikify-each.json', 'r') as fp:
    wikified = json.load(fp)

for e in wikified:
    for i in e['imgs'].values():
        nice.get(i['url'])
