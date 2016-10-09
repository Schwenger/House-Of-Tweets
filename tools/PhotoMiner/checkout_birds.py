#!/usr/bin/env python3

# NOTE: Before running this script, you may want to either get my cache,
# or run 'fetch.py' from the branch 'crawler-fetch'.

import json
import nice
import os
import checkout_hot_poli
from shutil import copyfile

RESOLUTION_PUBWEB = '200x150'
RESOLUTION_HOT = '330x330'

HOT_DIR_PREFIX = 'preview_hb'
os.mkdir(HOT_DIR_PREFIX)  # If this fails: you should always start from scratch here!


def checkout(bid, fields):
    GRAVITY_NORTH = {
        'buntspecht',
        'girlitz',
        'grauschnaepper',
        'mehlschwalbe',
    }
    gravity = 'center'
    if bid in GRAVITY_NORTH:
        gravity = 'north'

    pubweb_prefix = os.path.join(checkout_hot_poli.DIR_PREFIX, bid)
    hot_prefix = os.path.join(HOT_DIR_PREFIX, bid)
    dl_path = nice.get(fields['url'])

    # Provide ready-to-use image for pubweb
    checkout_hot_poli.convert(dl_path,
        '-resize', RESOLUTION_PUBWEB + '^>',
        '-strip',
        # It shouldn't ever be necessary to actually cut down the image vertically.
        # However, the code should still do something reasonable.
        '-gravity', gravity,
        '-extent', RESOLUTION_PUBWEB + '>',
        pubweb_prefix + '.jpg')

    # Provide ready-to-use images for HoT
    checkout_hot_poli.convert(dl_path,
        '-resize', RESOLUTION_HOT + '^>',
        '-strip',
        # It shouldn't ever be necessary to actually cut down the image vertically.
        # However, the code should still do something reasonable.
        '-gravity', gravity,
        '-extent', RESOLUTION_HOT + '>',
        hot_prefix + '.jpg')
    copyfile(hot_prefix + '.jpg', hot_prefix + '-drawing.jpg')

    entry = {
        'filename': bid + '.jpg',
        'license': fields['license'],
    }
    if 'copyright' in fields:
        entry['copyright'] = fields['copyright']

    return entry


def run():
    with open('fetch_birds.json', 'r') as fp:
        birds = json.load(fp)

    result = []
    # Arbitrary order for reproducability
    for bid, bird in sorted(birds.items(), key=lambda x: x[1]['de_name']):
        print('[INFO] Checking out files for ' + bird['de_name'])
        entry = checkout(bid, bird['img'])
        entry['bid'] = bid
        entry['de_name'] = bird['de_name']
        entry['en_name'] = bird['en_name']
        result.append(entry)

    with open('checkout_pubweb_birds.json', 'w') as fp:
        json.dump(result, fp, sort_keys=True, indent=2)


if __name__ == '__main__':
    run()
    print('Done.')
