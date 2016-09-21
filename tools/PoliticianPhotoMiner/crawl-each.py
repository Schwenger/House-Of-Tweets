#!/usr/bin/env python3

import nice
import json


def crawl_pages_inplace(data):
    for entry in data:
        assert 'page_file' not in entry
        entry['page_file'] = nice.get(entry['page'])


if __name__ == '__main__':
    with open("parse-roots.json", 'r') as fp:
        pages = json.load(fp)
    # Modifies 'pages':
    crawl_pages_inplace(pages)
    with open("crawl-each.json", 'w') as fp:
        json.dump(pages, fp, sort_keys=True, indent=2)
