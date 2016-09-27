#!/usr/bin/env python3

# NOTE: Before running this script, you may want to either get my cache,
# or run 'fetch.py' from the branch 'crawler-fetch'.

import json
import nice
import os
import checkout_images


def checkout(bid, fields):
    img_prefix = os.path.join(checkout_images.DIR_PREFIX, bid)
    dl_path = nice.get(fields['url'])
    freshest_path = dl_path

    # Provide ready-to-use image
    checkout_images.convert(freshest_path,
        '-resize', '259x500^>',
        # It shouldn't ever be necessary to actually cut down the image.
        # However, the code should still do something reasonable.
        '-gravity', 'center',
        '-extent', '259x500',
        img_prefix + '.jpg')

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
        result.append(entry)

    with open('checkout_birds.json', 'w') as fp:
        json.dump(result, fp, sort_keys=True, indent=2)


if __name__ == '__main__':
    run()
    print('Done.')
