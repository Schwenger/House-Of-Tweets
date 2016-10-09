#!/usr/bin/env python3

# NOTE: Before running this script, you may want to either get my cache,
# or run 'fetch.py' from the branch 'crawler-fetch'.

import json
import nice
import os
import checkout_hot_poli

OVERRIDE_COPYRIGHT = {
    'mehlschwalbe': ('English: Uploaded by Aelwyn with', 'Aelwyn'),
    'tannenmeise': ('This illustration was made by Marek Szczepanek\n', 'Marek Szczepanek'),
    'dohle': ('Frank Liebig \n\n\n', 'Frank Liebig'),
    'kleiber': ('Dave Menke (1946\u20132011) \u00a0\n\n', 'Dave Menke'),
    'buchfink': ('Self: Commons user MichaelMaggs', 'Michael Maggs'),
}
UNUSED_COPYRIGHT = dict(OVERRIDE_COPYRIGHT)

RESOLUTION = '200x150'


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

    img_prefix = os.path.join(checkout_hot_poli.DIR_PREFIX, bid)
    dl_path = nice.get(fields['url'])
    freshest_path = dl_path

    # Provide ready-to-use image
    # A width of *exactly* 259 pixels is imposed by the table layout switching.
    # The minimum height of 152 is arbitrary, but for reference:
    #   for 4x3 you need 194 vertical pixels,
    #   for 16x9 you need 146.
    #   So I went with
    checkout_hot_poli.convert(freshest_path,
        '-resize', RESOLUTION + '^>',
        '-strip',
        # It shouldn't ever be necessary to actually cut down the image vertically.
        # However, the code should still do something reasonable.
        '-gravity', gravity,
        '-extent', RESOLUTION + '>',
        img_prefix + '.jpg')

    entry = {
        'filename': bid + '.jpg',
        'license': fields['license'],
    }
    if 'copyright' in fields:
        entry['copyright'] = fields['copyright']

    if bid in OVERRIDE_COPYRIGHT:
        expected_start, copyright_new = OVERRIDE_COPYRIGHT[bid]
        actual = entry['copyright']
        if actual is not None and actual.startswith(expected_start):
            print('[WARN] Overriding copyright for ' + bid)
            entry['copyright'] = copyright_new
            del UNUSED_COPYRIGHT[bid]
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
    assert len(UNUSED_COPYRIGHT) == 0, UNUSED_COPYRIGHT

    with open('checkout_pubweb_birds.json', 'w') as fp:
        json.dump(result, fp, sort_keys=True, indent=2)


if __name__ == '__main__':
    run()
    print('Done.')
