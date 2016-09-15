#!/usr/bin/env python3

# Output format:
# [
#   { "party": "spd", "link": "https://whatever", "filename": "object_1234.dat" }
#   …
# ]
# Each of the fetch_* functions returns something that
# could be / will be a subset of the 'content' field.
# 'party' may be null, if this entry was fetched from bundestag.de.

import nice
import json


def construct_root(party, url):
    return {'party': party, 'link': url, 'filename': nice.get(url)}


def fetch_bundestag():
    accu = []
    # This enumeration of letters is correct because:
    # - The list for unused letters will be empty, not an error page
    # - Politicians with a starting Umlaut are sorted into the
    #   respective "normal" letter's page.
    akku = []
    for o in range(ord('A'), ord('Z') + 1):
        char = chr(o)
        url = 'https://www.bundestag.de/bundestag/abgeordnete18/biografien/' + str(char)
        akku.append(construct_root(None, url))
    return akku


def fetch_gruene():
    url = 'https://www.gruene-bundestag.de/abgeordnete.html'
    return [construct_root('gruene', url)]


def fetch_linke():
    prefix = 'https://www.linksfraktion.de/fraktion/abgeordnete/'
    parts = ["a-bis-e/", "f-bis-j/", "k-bis-o/", "p-bis-t/", "u-bis-z/"]
    akku = []
    for part in parts:
        url = prefix + part
        akku.append(construct_root('die linke', url))
    return akku


def fetch_spd():
    url = 'http://www.spdfraktion.de/abgeordnete/alle?wp=18&view=grid&old=18'
    return [construct_root('spd', url)]


def fetch_cxu():
    url = 'https://www.cducsu.de/abgeordnete/'
    return [construct_root('cxu', url)]


if __name__ == '__main__':
    all_entries = []
    all_entries.extend(fetch_linke())
    all_entries.extend(fetch_gruene())
    all_entries.extend(fetch_spd())
    all_entries.extend(fetch_cxu())
    all_entries.extend(fetch_bundestag())  # Slowest last
    with open("crawl-roots.json", 'w') as fp:
        json.dump(all_entries, fp, sort_keys=True, indent=2)
