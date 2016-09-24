#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json
import nice

USE_URLS = [
    # You have to spoof these pages, as some content gets loaded dynamically.
    # This is also why it's not part of the "supported" chain.
    'https://twitter.com/dieLinke/lists/parteivorstand/members',
    'https://twitter.com/cducsubt/lists/mdb/members',
    'https://twitter.com/spdde/lists/unser-team-im-kabinett/members',
]

new_handles = 0

def merge_handle(entry, new_handle):
    # Set of known-outdated Twitter-accounts:
    twitter_outdated = {
        'peternachberlin',
        'GabiKatzmarek',
    }
    assert new_handle not in twitter_outdated
    if 'twittering' not in entry:
        entry['twittering'] = {'twitterUserName': new_handle}
        print('[INFO] New handle {} for {}'.format(new_handle, entry['name']))
        global new_handles
        new_handles += 1
    else:
        old_handle = entry['twittering']['twitterUserName']
        assert old_handle.lower() == new_handle.lower(), (old_handle, new_handle)


def as_soup(path):
    # I'm fully aware that loading directly from the response content might be
    # faster, but this guarantees that the "filesystem cache"-thing actually works.
    with open(path, 'r') as fp:
        return BeautifulSoup(fp.read(), 'html.parser')


# Returns a set with the two longest "words" out of name.
def important_parts(name):
    def by_inv_len(s):
        return -len(s), s

    parts = sorted(name.split(), key=by_inv_len)
    important = tuple(parts[:4])
    important = [s for s in important if len(s) >= 3]
    assert len(important) >= 2, name  # Arbitrary
    return tuple([s.lower() for s in important])


def find_poli(name, by_parts):
    ignored = dict()
    for parts, poli in by_parts.items():
        assert len(parts) > 1, parts
        matches = len([p for p in parts if p in name.lower()])
        real_name = poli['name']
        if matches == 1:
            ignored[real_name] = poli
        elif matches >= 2:
            if name != real_name:
                print('[INFO] Match found: real {} <-> {} twitter'.format(real_name, name))
            return poli
    if len(ignored) == 1:
        real_name, poli = list(ignored.items())[0]
        print('[WARN] Allow near-match: real {} <-> {} twitter'.format(real_name, name))
        return poli
    for real_name in ignored.keys():
        print('[WARN] Ignoring near match {} (searching for {})'.format(real_name, name))
    return None


IGNORE_PEOPLE = {
    'Franziska Riekewald',
    'Miriam Strunge',
    '(((Klaus Lederer)))',
    'Junge Gruppe',
    'Arne Brix',
    'Manuela Schwesig',  # She's in the Landtag, but not Bundestag
    'Hans-Georg von der Marwitz',  # He doesn't use Twitter, and causes non-deterministic false positives
}

RESOLVE_MANUAL = {
    'Christian v. Stetten': 'Christian Freiherr von Stetten',
}


def run():
    with open('converge-each.json', 'r') as fp:
        polis = json.load(fp)
    by_parts = {important_parts(e['name']): e for e in polis}

    for url in USE_URLS:
        print('[INFO] Beginning with ' + url)
        accounts = 0
        accounts_unresolved = 0
        soup = as_soup(nice.get(url))
        for account in soup.find(id='timeline').find_all(None, 'js-user-profile-link'):
            accounts += 1
            name = account.find(None, 'fullname').get_text().strip()
            if name in IGNORE_PEOPLE:
                continue
            if name in RESOLVE_MANUAL:
                name = RESOLVE_MANUAL[name]
            poli = find_poli(name, by_parts)
            if poli is None:
                print('[WARN] Couldn\'t resolve ' + name)
                accounts_unresolved += 1
            else:
                handle = account.find(None, 'username').get_text().strip().strip('@')
                merge_handle(poli, handle)

        print('[INFO] Done. Seen {} accounts, {} of them unresolved.'
              .format(accounts, accounts_unresolved))

    print('[INFO] Done overall. Seen {} new handles.'.format(new_handles))
    with open('twitter-each.json', 'w') as fp:
        json.dump(polis, fp, sort_keys=True, indent=2)


if __name__ == '__main__':
    run()
