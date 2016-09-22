#!/usr/bin/env python3

import nice
import json
import re
from bs4 import BeautifulSoup


# Annoying people that are annoying.
url_override = {
    # Wikipedia doesn't list them with their 'name' as per bundestag.de:
    'https://de.wikipedia.org/wiki/Andreas_G._Lämmel': 'https://de.wikipedia.org/wiki/Andreas_L%C3%A4mmel',
    'https://de.wikipedia.org/wiki/Karl-Heinz_Helmut_Wange': 'https://de.wikipedia.org/wiki/Karl-Heinz_Wange',
    # Badly written disambiguation page:
    'https://de.wikipedia.org/wiki/Christian_Petry': 'https://de.wikipedia.org/wiki/Christian_Petry_(Politiker)',
}

known_missing = {
    'Iris Ripsam',
    'Karl-Heinz Helmut Wange',
}


# Returns True or False
def is_not_found(soup):
    return soup.find('div', id='noarticletext') is not None


# Returns:
# - None: not a disambiguation page
# - some string: actual url
# If it is a disambiguation page, all implicit assumptions will be 'assert'-ed.
def get_disambiguated_url(soup, expect_party):
    PARTY_TO_TEXT = {
        'spd': 'SPD', 'csu': 'CSU', 'cdu': 'CDU', 'die linke': 'Die Linke',
        'gruene': 'Bündnis 90/Die Grünen',
    }
    if soup.find('table', id='Vorlage_Begriffsklaerung') is None:
        return None
    content = soup.find('div', id='mw-content-text')
    assert content is not None
    ul = content.find('ul')
    assert ul is not None
    print('[WARN] Hit disambiguation page')
    found_urls = []
    # FIXME: why does pattern.match require the leading and trailing .*?
    # I would expect that behavior with fullmatch, but not with match.
    pattern = re.compile('.*\(\d{4}[-–—]\d{4}\).*')
    found_mdb = None
    for li in ul.find_all('li'):
        text = li.get_text()
        if 'Politiker' not in text:
            continue
        if 'MdB' in text or 'Bundestag' in text:
            assert found_mdb is None, found_mdb
            a = li.find('a')
            assert a is not None
            # Let's hope the href-scheme doesn't change too soon:
            found_mdb = 'https://de.wikipedia.org' + a['href']
        if PARTY_TO_TEXT[expect_party] not in text:
            # Don't just print 'text', as I might need that URL.
            print('[WARN] Found someone of wrong party: {}'.format(li))
            continue
        if '(MdL)' in text:
            # Don't just print 'text', as I might need that URL.
            print('[WARN] Ignore Landtag politician: {}'.format(li))
            continue
        if pattern.match(text) is not None:
            # Don't just print 'text', as I might need that URL.
            print('[WARN] Ignore dead person: {}'.format(li))
            continue
        a = li.find('a')
        assert a is not None
        # Let's hope the href-scheme doesn't change too soon:
        found_urls.append('https://de.wikipedia.org' + a['href'])
    assert len(found_urls) >= 1, (found_urls, ul)
    if len(found_urls) == 1:
        return found_urls[0]
    assert found_mdb is not None, (found_urls, ul)
    print('[WARN] Using MdB override')
    return found_urls[0]


def as_soup(path):
    with open(path, 'r') as fp:
        return BeautifulSoup(fp.read(), 'html.parser')


# Returns either the path to the "real" document, or None if no such thing found.
def crawl_page_for(name, expect_party):
    # Minuses and Umlauts can stay.  Hooray!
    urlish_name = name.replace(' ', '_')
    url = 'https://de.wikipedia.org/wiki/' + urlish_name
    if url in url_override:
        print('[WARN] Using override for ' + name)
        url = url_override[url]
    path = nice.get(url)
    soup = as_soup(path)
    if is_not_found(soup):
        if name in known_missing:
            print('[WARN] Not found (and whitelisted): ' + name)
        else:
            print('[ERR!] Unexpectedly not found: ' + name)
            raise AssertionError(name)
        return None
    disambig_url = get_disambiguated_url(soup, expect_party)
    if disambig_url is None:
        return path
    url = disambig_url
    path = nice.get(url)
    soup = as_soup(path)
    if is_not_found(soup):
        # This really, really should not happen.
        # Let's hope that female politicians don't have 'Politikerin' as disambiguation.
        print('[ERR!] Confused about: ' + name)
        raise AssertionError(path)
    # This wouldn't even make sense, or at least there is hopefully only one
    # politician for each name.  Note that other parts of this toolchain fail
    # horribly in this case anyway.
    assert get_disambiguated_url(soup, expect_party) is None, 'name'
    return path


def run():
    with open("aggregate-each.json", 'r') as fp:
        crawled = {e['full_name']: crawl_page_for(e['name'], e['party'])
                   for e in json.load(fp)}
    with open("crawl-wiki.json", 'w') as fp:
        json.dump(crawled, fp, sort_keys=True, indent=2)


if __name__ == '__main__':
    run()
