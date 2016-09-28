#!/usr/bin/env python3

import json


def strip_birds(birds_raw):
    COPY_FIELDS = ['bid', 'de_name', 'en_name']
    return [{k: v for k, v in b.items() if k in COPY_FIELDS} for b in birds_raw]


def run():
    with open('../PhotoMiner/checkout_birds.json', 'r') as fp:
        birds = json.load(fp)
    stripped_birds = strip_birds(birds)
    with open('birds.coffee', "w") as out:
        out.write("RawBirds = ")
        json.dump(stripped_birds, out, sort_keys=True, indent="\t")


if __name__ == '__main__':
    run()
