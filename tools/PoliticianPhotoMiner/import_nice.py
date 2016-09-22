#!/usr/bin/env python3

import json
import nice
import os.path


nice._load_cache()
entries = nice._cache['entries']
nice._cache['last_change'] = 'BULK IMPORT'


def spoof(url, old_path):
    global entries
    new_path = 'cache/' + old_path
    assert url not in entries
    assert os.path.isfile(new_path)
    entries[url] = new_path


if False:
    with open('crawl-roots.json', 'r') as roots_fp:
        PREFIX = '/home/eispin/workspace/House-Of-Tweets/tools/PoliticianPhotoMiner/'
        for e in json.load(roots_fp):
            assert e['filename'].startswith(PREFIX)
            spoof(e['link'], e['filename'][len(PREFIX):])

if False:
    with open('crawl-each.json', 'r') as each_fp:
        for e in json.load(each_fp):
            spoof(e['page'], e['page_file'])

if False:
    with open('crawl-wiki.log.json', 'r') as each_fp:
        for url, file in json.load(each_fp).items():
            spoof(url, file)

nice._write_cache()
