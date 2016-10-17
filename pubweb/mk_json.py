#!/usr/bin/env python3

# General idea: split up the birds in a *single* place
# so that nothing can go wrong.

import json

# We have at most 4 columns, and for a 1280x1024 monitor you currently can
# see three rows [1], so we need to load 4+4+1=9 birds initially, at least.
# [1]: I figured that out empirically.
#      TODO: Figure out if there's a better way to do it.
INIT_DISPLAY_AMOUNT = 9


def strip_bird(bird, lang):
    # BID, display name, Tweet name
    return [bird['bid'], bird[lang + '_name'], bird['de_name']]


def deal_birds(birds, lang):
    def by_name(bird):
        return bird[lang + '_name']
    stripped_birds = [strip_bird(b, lang) for b in sorted(birds, key=by_name)]
    with open('birds_' + lang + '_init.json', "w") as out:
        json.dump(stripped_birds[:INIT_DISPLAY_AMOUNT], out, indent=2)
    with open('birds_' + lang + '_dyn.coffee', "w") as out:
        out.write('RawBirds_' + lang + ' = ')
        json.dump(stripped_birds[INIT_DISPLAY_AMOUNT:], out, indent="\t")


def run():
    with open('../tools/PhotoMiner/checkout_pubweb_birds.json', 'r') as fp:
        birds = json.load(fp)
    deal_birds(birds, 'de')
    deal_birds(birds, 'en')


if __name__ == '__main__':
    run()
