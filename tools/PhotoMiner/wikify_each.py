#!/usr/bin/env python3

import nice
import json
import re
from bs4 import BeautifulSoup


url_override = {
    # Badly written disambiguation page:
    'https://de.wikipedia.org/wiki/Christian_Petry': 'https://de.wikipedia.org/wiki/Christian_Petry_(Politiker)',
    'https://de.wikipedia.org/wiki/Charles_Huber': 'https://de.wikipedia.org/wiki/Charles_M._Huber',
    # Wikipedia doesn't list him with his 'name' as per bundestag.de:
    'https://de.wikipedia.org/wiki/Karl-Heinz_Helmut_Wange': 'https://de.wikipedia.org/wiki/Karl-Heinz_Wange',
    'https://de.wikipedia.org/wiki/Gerd_Müller': 'https://de.wikipedia.org/wiki/Gerd_M%C3%BCller_%28CSU%29',
    # Bad default:
    'https://de.wikipedia.org/wiki/Andreas_Rimkus': 'https://de.wikipedia.org/wiki/Andreas_Rimkus_(Politiker)',
    'https://de.wikipedia.org/wiki/Karl_Lamers': 'https://de.wikipedia.org/wiki/Karl_A._Lamers',
    'https://de.wikipedia.org/wiki/Michael_Groß': 'https://de.wikipedia.org/wiki/Michael_Gro%C3%9F_%28Politiker%29',
    'https://de.wikipedia.org/wiki/Peter_Stein': 'https://de.wikipedia.org/wiki/Peter_Stein_%28Politiker%29',
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
        'SPD': 'SPD', 'CSU': 'CSU', 'CDU': 'CDU', 'DIE LINKE': 'Die Linke',
        'GRÜNE': 'Bündnis 90/Die Grünen',
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
    death_pattern = re.compile('.*\(\d{4}[-–—]\d{4}\).*')
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
        if death_pattern.match(text) is not None:
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
    return found_mdb


def as_soup(path):
    # I'm fully aware that loading directly from the response content might be
    # faster, but this guarantees that the "filesystem cache"-thing actually works.
    with open(path, 'r') as fp:
        return BeautifulSoup(fp.read(), 'html.parser')


# Returns either the soup of the "real" document, or None if no such thing found.
def get_page_for(name, expect_party):
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
        return url, soup
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
    return url, soup


def get_img_desc_link(name, page_soup):
    outer_div = page_soup.find('div', 'thumbinner')
    # Pages where the "image" is not usable (e.g., is actually a video)
    IMG_BLACKLIST = {
        'Carsten Träger',  # is a video
        'Heiko Schmelzle',  # is a video
        'Marina Kermer',  # is a video
    }
    # If there's no image at all, that's fine.
    if outer_div is None or name in IMG_BLACKLIST:
        return None

    # Pages where the image description is "unexpected"
    IMG_WHITELIST = {
        'Burkhard Lischka',  # bullshit
        'Cajus Caesar',  # Gajus
        'Charles Huber',  # M.
        'Christian Freiherr von Stetten',  # no 'Freiherr'
        'Christian Kühn',  # Chris
        'Johann David Wadephul',  # No 'David'
        'Karl Lamers',  # A.
        'Karin Evers-Meyer',  # Typo in description
        'Matthias Birkwald',  # W.
        'Norbert Spinrath',  # Typo in description
        'Philipp Graf Lerchenfeld',  # Philipp Graf von und zu Lerchenfeld is a very special von und zu snowflake.
        'Ulli Nissen',  # Ulrike vs. Ulli
        'Waltraud Wolff',  # "Wahlkampfmotiv 2013" is actually quite sensible!
    }
    # Sanity check to see whether it's actually a photo of that person:
    assert name in outer_div.get_text() or name in IMG_WHITELIST, page_soup.title

    inner_div = outer_div.find('div', 'magnify')
    # There should always be a "magnify" link.  I hope.
    assert inner_div is not None, page_soup.title

    a = inner_div.find('a', 'internal')
    # And it should have an internal link to the page that describes the image.  I hope.
    assert a is not None, page_soup.title
    # href="/wiki/Datei:Bahr,_Ulrike-9287.jpg"
    # becomes https://de.wikipedia.org/wiki/Datei:Bahr,_Ulrike-9287.jpg

    return 'https://de.wikipedia.org' + a['href']


# Retrieve the copyright *holder* information, or in German: "Urheber".
# This is orthogonal to the license/permissions information.
def parse_copyright(soup):
    # "_aut" means: author information.  This is what we are looking for.
    author_td = soup.find(id='fileinfotpl_aut')  # Sometimes td, sometimes th
    assert author_td is not None, "No copyright holder for file?!"
    assert author_td.name in ['td', 'th'], author_td
    # However, the author is stored in the adjacent HTML table-cell,
    # as author_td itself is non-informative.
    author_text = author_td.parent.get_text()
    prefixes = ['\nUrheber\n',
                '\nUrheber bzw.\nNutzungsrechtinhaber\n',
                '\nFotograf\n',
                '\nAuthor\n'
                ]
    for prefix in prefixes:
        if author_text.startswith(prefix):
            return author_text[len(prefix):].strip()
    assert False, author_text


KNOWN_LICENSES = {
    'Der Urheberrechtsinhaber erlaubt es jedem, dieses Werk für jeglichen Zweck, inklusive uneingeschränkter Weiterveröffentlichung, kommerziellem Gebrauch und Modifizierung, zu nutzen.': 'public domain',
    'erlaubt es jedem, diese für jeden Zweck zu benutzen, vorausgesetzt, dass der Urheberrechtsinhaber ordnungsgemäß genannt wird.': 'public domain',
    'Der Urheber gestattet jedermann jede Form der Nutzung, unter der Bedingung der angemessenen Nennung seiner Urheberschaft.\nWeiterverbreitung, Bearbeitung und kommerzielle Nutzung sind gestattet.': 'custom: attribution',
    'Lizenz „Freie Kunst“': 'custom: attribution (FAL)',
    'GNU-Lizenz für freie Dokumentation, Version 1.2,': 'GFDL 1.2',
    'GNU-Lizenz für freie Dokumentation, Version 1.2 oder einer späteren Version': 'GFDL 1.2+',
    '\nPublic domainPublic domainfalsefalse\n\n': 'public domain',
    'Creative-Commons-Lizenz „CC0 1.0 Verzicht auf das Copyright“': 'CC0 1.0',
    # Include the closing quotation mark to ensure unambiguous identification.
    'Creative-Commons-Lizenz „Namensnennung 2.0 generisch“': 'CC-BY-2.0',
    'Creative-Commons-Lizenz „Namensnennung 2.0 Deutschland“': 'CC-BY-2.0 de',
    'Creative-Commons-Lizenz „Namensnennung 3.0 nicht portiert“': 'CC-BY-3.0 unported',
    'Creative-Commons-Lizenz „Namensnennung 3.0 Deutschland“': 'CC-BY-3.0 de',
    'Creative-Commons-Lizenz „Namensnennung 4.0 international“': 'CC-BY-4.0 int',
    'Creative-Commons-Lizenz „Namensnennung – Weitergabe unter gleichen Bedingungen 2.0 generisch“': 'CC-BY-SA-2.0',
    'Creative Commons Attribution-Share Alike 2.0 Generic license.': 'CC-BY-SA-2.0',
    'Creative-Commons-Lizenz „Namensnennung – Weitergabe unter gleichen Bedingungen 2.0 Deutschland“': 'CC-BY-SA-2.0 de',
    'http://creativecommons.org/licenses/by-sa/2.0/de/legalcode': 'CC-BY-SA-2.0 de',
    'Creative-Commons-Lizenz „Namensnennung – Weitergabe unter gleichen Bedingungen 2.5 generisch“': 'CC-BY-SA-2.5',
    'Creative-Commons-Lizenzen „Namensnennung – Weitergabe unter gleichen Bedingungen 2.5 generisch“': 'CC-BY-SA-2.5',
    # If multiple versions available, use the first one
    'Creative-Commons-Lizenzen „Namensnennung – Weitergabe unter gleichen Bedingungen 3.0 nicht portiert“': 'CC-BY-SA-3.0- unported',
    'http://creativecommons.org/licenses/by-sa/3.0/legalcode': 'CC-BY-SA-3.0 unported',
    'Creative-Commons-Lizenz „Namensnennung – Weitergabe unter gleichen Bedingungen 3.0 nicht portiert“': 'CC-BY-SA-3.0 unported',
    'Creative-Commons-Lizenz „Namensnennung – Weitergabe unter gleichen Bedingungen 3.0 Deutschland“': 'CC-BY-SA-3.0 de',
    'Creative-Commons-Lizenz „Namensnennung – Weitergabe unter gleichen Bedingungen 3.0 Österreich“': 'CC-BY-SA-3.0 at',
    'Creative-Commons-Lizenz „Namensnennung – Weitergabe unter gleichen Bedingungen 4.0 international“': 'CC-BY-SA-4.0 int',
}

LICENSE_PREFERENCE_ORDER = [
    'public domain',
    'CC0 1.0',
    'CC-BY-SA-4.0 int',
    'CC-BY-4.0 int',
    'CC-BY-SA-3.0 de',
    'CC-BY-SA-3.0 unported',
    'CC-BY-SA-3.0 at',
    'CC-BY-SA-3.0- unported',
    'CC-BY-3.0 de',
    'CC-BY-3.0 unported',
    'CC-BY-SA-2.5',
    'CC-BY-SA-2.0 de',
    'CC-BY-SA-2.0',
    'CC-BY-2.0 de',
    'CC-BY-2.0',
    'GFDL 1.2+',
    'GFDL 1.2',
    'custom: attribution (FAL)',
    'custom: attribution',
]


def assert_license_sanity():
    # With that function name, I'm very willing to just write "assert False"
    for lid in KNOWN_LICENSES.values():
        assert lid in LICENSE_PREFERENCE_ORDER, lid


# Parse "the" license of the file.
def parse_license(soup):
    all_licenses = []
    for license_table in soup.find_all(None, 'licensetpl'):  # not always a table
        license_text = license_table.get_text()
        found = False
        for text, lid in KNOWN_LICENSES.items():
            if text in license_text:
                assert not found, 'Multiple contradicting licenses within same paragraph?!'
                all_licenses.append(lid)
                found = True
                assert lid in LICENSE_PREFERENCE_ORDER, lid
                # Don't break, check for duplicates!
        assert found, license_text  # If this fails, add a new entry in KNOWN_LICENSES
    assert len(all_licenses) > 0
    for l in LICENSE_PREFERENCE_ORDER:
        if l in all_licenses:
            return l
    assert False, all_licenses


def parse_img_url(soup):
    wrapper_div = soup.find('div', 'fullImageLink')
    a = wrapper_div.find('a')
    # given: //upload.wikimedia.org/wikipedia/commons/8/88/Portr%C3%A4t_Wolfgang_Hellmich.jpg
    # Link: https://upload.wikimedia.org/wikipedia/commons/8/88/Portr%C3%A4t_Wolfgang_Hellmich.jpg
    return 'https:' + a['href']


# Returns an 'imgs' entry.
def get_img_desc(img_desc_url):
    path = nice.get(img_desc_url)
    soup = as_soup(path)
    return {
        'copyright': parse_copyright(soup),
        'license': parse_license(soup),
        'url': parse_img_url(soup),
    }


WHITELIST_AMBIGUOUS = {
    'Angela Merkel',
    'Cajus Caesar',
    'Carsten Müller',
    'Cem Özdemir',
    'Christian Schmidt',  # There's another politician "B" of this name.  I don't mean B.
    'Joachim Pfeiffer',
    'Kristina Schröder',
    'Sascha Raabe',
    'Thomas Feist',
    'Gernot Erler',
    'Jens Koeppen',
    'Johannes Kahrs',
    'Klaus Ernst',
    'Manfred Grund',
    'Michael Brand',
    'Peter Altmaier',
    'Sibylle Pfeiffer',
    'Stephan Mayer',
    'Ulla Schmidt',
    'Volker Beck',
}


SPOOF_POLITICIANS = [
    ('Barack Obama', 'Demokraten', 'barackobama'),
    ('François Hollande', 'Parti socialiste', 'fhollande'),
    # Can't spoof HoT sufficiently well
]


def run():
    with open("aggregate_each.json", 'r') as fp:
        entries = json.load(fp)
    for e in entries:
        name = e['name']
        orig_name = name
        name = re.sub(' [A-ZÖÄÜ]\. ', ' ', name)
        if name != orig_name:
            print('[WARN] Sanitized name {} to {}'.format(orig_name, name))
        findings = get_page_for(name, e['party'])
        if findings is None:
            continue
        page_url, page_soup = findings
        e['srcs']['wiki'] = page_url
        if page_soup.find(id='bksicon') is not None and name not in WHITELIST_AMBIGUOUS:
            print('[WARN] Name {} is ambiguous, but wasn\'t asked to choose'.format(name))
        img_desc_url = get_img_desc_link(name, page_soup)
        if img_desc_url is None:
            # No image?  Okay :(
            continue
        e['imgs']['wiki'] = get_img_desc(img_desc_url)
    for name, party, handle in SPOOF_POLITICIANS:
        e = dict(name=name, full_name=name, party=party, handle=handle,
                 srcs=dict(), imgs=dict())
        entries.append(e)
        findings = get_page_for(name, e['party'])
        assert findings is not None
        page_url, page_soup = findings
        e['srcs']['wiki'] = page_url
        # ignore 'bksicon'
        img_desc_url = get_img_desc_link(name, page_soup)
        assert img_desc_url is not None
        e['imgs']['wiki'] = get_img_desc(img_desc_url)

    with open("wikify_each.json", 'w') as fp:
        json.dump(entries, fp, sort_keys=True, indent=2)


if __name__ == '__main__':
    assert_license_sanity()
    run()
    print('Done.')
