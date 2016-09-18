#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import json


# Sorry for the massive code duplication, but I'd rather keep the parsers strictly
# separated than creating one big, hairy parser with lots of optional arguments.

def get_polis_bundestag(soup):
    # Could be compiled globally, but don't pollute namespace
    # FIXME: Some politicians have different URLs!
    pat = re.compile('^/bundestag/abgeordnete18/biografien/./(-|[a-z_]+)/\d+$')
    # Example:
    # <a href="/bundestag/abgeordnete18/biografien/U/uhl_hans_peter/259136" title="linkTextAttr">
    #   Uhl, Dr. Hans-Peter, CDU/CSU
    # </a>
    # Alternative href:
    #   /bundestag/abgeordnete18/biografien/C/-/438482
    for a in soup.find_all('a'):
        href = a.get('href')
        match = None
        if href is not None:
            match = pat.match(href)
        if match is None:
            if href is not None \
                    and href.startswith('/bundestag/abgeordnete18/bio') \
                    and len(href) > len('/bundestag/abgeordnete18/biografien/X'):
                print('Ignoring "irrelevant" href "{}"'.format(href))
            continue
        text = a.get_text().strip()
        # == Reconstruct "simple" name without titles ==
        # Assume this is the full, true name
        parts = match.groups()[0].split('_')
        parts = [s.capitalize() for s in parts]
        # Rebuild from the stupid "Last first second" order
        name = ' '.join(parts[1:] + parts[:1])
        # == Reconstruct "full" name, *with* titles ==
        parts = text.split(', ')
        full_name = ' '.join(parts[1:-1] + parts[:1])
        detect_party = parts[-1]
        # Hope that the href scheme doesn't change within the next days
        page = 'https://www.bundestag.de' + href
        entry = {'src': 'bundestag', 'name': name, 'full_name': full_name,
                 'page': page, 'detect_party': detect_party}
        yield entry


def get_polis_gruene(soup):
    # Could be compiled globally, but don't pollute namespace
    pat = re.compile('^abgeordnete/([a-z-]+)\.html$')
    # Example: <a href="abgeordnete/luise-amtsberg.html" class="content-teaser__blocklink">
    # … plus a bunch of inner elements, most importantly:
    # <h3 class="content-teaser__title">Luise Amtsberg</h3>
    for a in soup.find_all('a', 'content-teaser__blocklink'):
        href = a.get('href')
        match = None
        if href is not None:
            match = pat.match(href)
        if match is None:
            if href.startswith('abgeordnete/'):
                print('Ignoring "irrelevant" href "{}"'.format(href))
            continue
        slugname = ' '.join([w.capitalize()
                             for w in match.groups()[0].split('-')])
        full_name = a.find('h3', 'content-teaser__title')
        if full_name is None:
            print('No name-field for {}'.format(slugname))
            continue
        full_name = full_name.get_text().strip()
        # Not a bug: The "die grüne" website uses hrefs without leading slashes.
        page = 'https://www.gruene-bundestag.de/' + href
        # The "slugname" seems to stem from the full_name, and does not contain any
        # additional information.
        entry = {'src': 'gruene', 'full_name': full_name, 'page': page}
        yield entry


def get_polis_linke(soup):
    # Could be compiled globally, but don't pollute namespace
    pat = re.compile('^/fraktion/abgeordnete/profil/([a-z-]+)/$')
    # Example: <a href="/fraktion/abgeordnete/profil/jan-van-aken/">Jan van Aken</a>
    for a in soup.find_all('a'):
        href = a.get('href')
        match = None
        if href is not None:
            match = pat.match(href)
        if match is None:
            if href.startswith('/fraktion/abgeordnete/profil/'):
                print('Ignoring "irrelevant" href "{}"'.format(href))
            continue
        full_name = a.get_text().strip()
        # slugname = ' '.join([p.capitalize() for p in match.groups()[0].split('-')])
        # The "slugname" seems to stem from the full_name, and does not contain any
        # additional information.
        page = 'https://www.linksfraktion.de' + href
        entry = {'src': 'die linke', 'full_name': full_name, 'page': page}
        yield entry


def get_polis_spd(soup):
    # Could be compiled globally, but don't pollute namespace
    pat = re.compile('^/abgeordnete/([a-z-]+)\?wp=18$')
    # Example: <a href="/abgeordnete/annen?wp=18">  Niels Annen</a>
    for a in soup.find_all('a'):
        href = a.get('href')
        match = None
        name = a.get_text().strip()
        if href is not None:
            match = pat.match(href)
        bad_match = match is None
        bad_name = name == ''
        if bad_match or bad_name:
            href_meaningful = href is not None and href.startswith('/abgeordnete')
            if href_meaningful and not bad_name:
                print('Ignoring "irrelevant" href "{}"'.format(href))
            continue
        slug = match.groups()[0]
        # Dear SPD: Welcome to the 21th century, now start using https!
        page = 'http://www.spdfraktion.de' + href
        entry = {'src': 'spd', 'name': name, 'page': page, 'slug': slug}
        yield entry


def get_polis_cxu(soup):
    PREFIX = '/abgeordnete/'
    # Example: <a class="abgeordnete_wrapper_link" href="/abgeordnete/stephan-albani"></a>
    for a in soup.find_all('a', 'abgeordnete_wrapper_link'):
        href = a.get('href')
        if href is None or not href.startswith(PREFIX):
            print('Ignoring "irrelevant" href "{}"'.format(href))
            continue
        rawname = href[len(PREFIX):]
        name = ' '.join([p.capitalize() for p in rawname.split('-')])
        page = 'https://www.cducsu.de' + href
        entry = {'src': 'cxu', 'name': name, 'page': page}
        yield entry


if __name__ == '__main__':
    from sys import argv
    if len(argv) != 2:
        print('Expected precisely 1 argument (something like roots_147….json), got {} instead.'.format(len(argv)))
        exit(1)

    # Reading
    json_path = argv[1]  # Not a typo, argv[0] is the program name
    with open(json_path, 'r') as json_fp:
        roots = json.load(json_fp)

    # Parsing (setup)
    all_pols = []
    resolvers = {
        None: get_polis_bundestag,
        'die linke': get_polis_linke,
        'gruene': get_polis_gruene,
        'spd': get_polis_spd,
        'cxu': get_polis_cxu,
    }
    # Parsing (actual)
    for root in roots:
        resolver = resolvers.get(root['party'])
        if resolver is None:
            print('[WARN] skip for party {}'.format(root['party']))
            continue
        print('Analyzing with {resolver}: URL={url}'
              .format(url=root['link'], resolver=resolver))
        with open(root['filename'], 'r') as fp:
            the_soup = BeautifulSoup(fp.read(), 'html.parser')
        all_pols.extend(resolver(the_soup))

    # Write it out.
    with open('parse-roots.json', 'w') as fp:
        json.dump(all_pols, fp, sort_keys=True, indent=2)
    print('Done.')
