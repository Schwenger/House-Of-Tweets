#!/usr/bin/env python3

from soundGenerator import gen_bird
import json
import mylog
from time import sleep


def determine_bird_ids():
    with open('birds.json', 'r') as fp:
        bids = json.load(fp).keys()
    return sorted(list(bids))


def mk_lengths():
    # Minimal length: 10000 ms (hardcoded; 40 bytes)
    # Maximal length: 37000 ms (empiric; 148 bytes)
    return list([l * 250 for l in range(40, 148 + 1)])


BIRD_IDS = determine_bird_ids()
MOODS = ['neutral', 'fragend', 'aufgebracht']
LENGTHS = mk_lengths()

print('About to generate {} * {} * {} = {} combinations!'
      .format(len(BIRD_IDS), len(MOODS), len(LENGTHS), len(BIRD_IDS) * len(MOODS) * len(LENGTHS)))
print('(Waiting 5 seconds so you can terminate if you want to ...)')
sleep(5)

for bid in BIRD_IDS:
    mylog.info('===== NOW GENERATING FOR: {} ====='.format(bid))
    for mood in MOODS:
        for len_ms in LENGTHS:
            gen_bird(bid, mood, False, len_ms)
            gen_bird(bid, mood, True, len_ms)
    mylog.info('===== DONE WITH: {} ====='.format(bid))
