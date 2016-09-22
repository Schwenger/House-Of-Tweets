#!/usr/bin/env python3

import nice
import os.path


nice._load_cache()

bad = []

for url, path in nice._cache['entries'].items():
    if not os.path.isfile(path):
        bad.append((url, path))
assert len(bad) == 0, bad
