#!/usr/bin/env python3

# This is *a lot* like wikify_each.
# TODO: Some refactoring to abstract away the common parts?

import json
import nice
import wikify_each


# Returns:
# - None: not a disambiguation page
# - some string: actual url
# If it is a disambiguation page, all implicit assumptions will be 'assert'-ed.
def get_disambiguated_url(soup, latin_name):
    if soup.find('table', id='Vorlage_Begriffsklaerung') is None:
        return None
    content = soup.find('div', id='mw-content-text')
    assert content is not None
    ul = content.find('ul')
    assert ul is not None
    print('[WARN] Hit disambiguation page')
    found_eigentlich = None
    found_urls = []
    for li in ul.find_all('li'):
        text = li.get_text()
        if not any([x in text for x in ['Vogel', 'Vögel', latin_name]]):
            continue
        a = li.find('a')
        assert a is not None
        # Let's hope the href-scheme doesn't change too soon:
        url = 'https://de.wikipedia.org' + a['href']
        if '&action=edit&redlink=1' in url:
            print('[WARN] Ignoring relevant ' + url)
            continue
        found_urls.append(url)
        if 'wiki/Eigentlich' in url:
            assert found_eigentlich is None, (latin_name, found_eigentlich)
            found_eigentlich = url
    assert len(found_urls) >= 1, (found_urls, ul)
    if len(found_urls) == 1:
        return found_urls[0]
    assert found_eigentlich is not None, found_urls
    print('[WARN] Required "Eigentlich" override for ' + found_eigentlich)
    return found_eigentlich


def get_page_for(bird):
    url_override = {
        # There's both the Familie and the Art.
        # The Familie has a better photo.
        'Kleiber': 'https://de.wikipedia.org/wiki/Kleiber_%28Familie%29',
    }
    de_name = bird['de_name']
    if de_name in url_override:
        url = url_override[de_name]
    else:
        # Minuses and Umlauts can stay.  Hooray!
        urlish_name = de_name.replace(' ', '_')
        url = 'https://de.wikipedia.org/wiki/' + urlish_name
    path = nice.get(url)
    soup = wikify_each.as_soup(path)
    if wikify_each.is_not_found(soup):
        print('[ERR!] Unexpectedly not found: ' + de_name)
        raise AssertionError(de_name)
    disambig_url = get_disambiguated_url(soup, bird['latin_name'])
    if disambig_url is None:
        return url, soup
    url = disambig_url
    path = nice.get(url)
    soup = wikify_each.as_soup(path)
    if wikify_each.is_not_found(soup):
        # This really, really should not happen.
        # Let's hope that female politicians don't have 'Politikerin' as disambiguation.
        print('[ERR!] Confused about: ' + de_name)
        raise AssertionError(path)
    # This wouldn't even make sense.
    assert soup.find('table', id='Vorlage_Begriffsklaerung') is None
    return url, soup


def get_img_desc_link(name, page_soup):
    taxo_box = page_soup.find(id='Vorlage_Taxobox')
    assert taxo_box is not None

    # Pages where the image description is "unexpected"
    IMG_WHITELIST = {
        'Distelfink',
        'Rabenkrähe',  # Why is this one even listed as Rabenkrähe?!
        'Rotkehlchen',  # Inconsistency for the sake of fuck you.
    }
    a = taxo_box.find('a', 'image')
    assert a is not None, name
    if name not in IMG_WHITELIST:
        def contains_name(text):
            return name.lower() in text.lower()
        # Sanity check to see whether it's actually a photo of that bird:
        title_tag = taxo_box.find('th')
        assert contains_name(title_tag.get_text()), (name, taxo_box.find('th'))
        assert contains_name(a['title']), (name, a['title'])
    # href="/wiki/Datei:Bahr,_Ulrike-9287.jpg"
    # becomes https://de.wikipedia.org/wiki/Datei:Bahr,_Ulrike-9287.jpg
    return 'https://de.wikipedia.org' + a['href']


def run():
    IMG_OVERRIDE = {
        'Haussperling': 'https://de.wikipedia.org/wiki/Datei:Passer_domesticus_male_%2815%29.jpg',
        # 'Schneeeule': 'https://de.wikipedia.org/wiki/Datei:Bubo_scandiacus_(Linnaeus,_1758)_Male.jpg', # Bad image!
        'Schneeeule': 'https://de.wikipedia.org/wiki/Datei:Schneeeule.JPG',
        'Türkentaube': 'https://de.wikipedia.org/wiki/Datei:Streptopelia_decaocto;_Szczecin,_Poland_3.JPG',
        # FIXME: There's so many "Star"s out there, which one does the common citizen recognize best?
        'Star': 'https://en.wikipedia.org/wiki/File:Starling_(5503763150).jpg',
        'Grünfink': 'https://de.wikipedia.org/wiki/Datei:Greenfinch_Carduelis_chloris.jpg',
        'Mauersegler': 'https://de.wikipedia.org/wiki/Datei:Apus_apus_-Barcelona,_Spain-8_%281%29.jpg',
        # Optional, not sure if a good idea:
        'Mehlschwalbe': 'https://de.wikipedia.org/wiki/Datei:Delichon_urbica_NRM.jpg',
    }

    with open('../../backend/birds.json') as fp:
        birds = json.load(fp)

    for bird in sorted(birds.values(), key=lambda x: x['de_name']):
        name = bird['de_name']
        if name in IMG_OVERRIDE:
            # No warning as this is a "human" choice
            print('[INFO] Human selection, so not even looking at article: ' + name)
            img_desc_url = IMG_OVERRIDE[name]
            del IMG_OVERRIDE[name]
        else:
            page_url, page_soup = get_page_for(bird)
            img_desc_url = get_img_desc_link(name, page_soup)
        assert img_desc_url is not None, name
        bird['img'] = wikify_each.get_img_desc(img_desc_url)

    assert len(IMG_OVERRIDE) == 0, IMG_OVERRIDE
    with open("fetch_birds.json", 'w') as fp:
        json.dump(birds, fp, sort_keys=True, indent=2)


if __name__ == '__main__':
    run()
