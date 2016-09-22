import json
import os
import requests
import time

# Amount of seconds to wait between each download.
_NICE_WAIT_TIME = 5
# Minimal sleep time for grace, in seconds.
_MIN_SLEEP_TIME = 0.1

# Let's hope this is unique enough
_PREFIX = "cache/results_" + str(int(time.time() * 1000))
os.mkdir(_PREFIX)
print("Wrapping everything in " + _PREFIX)


_last_nice_poll = 0

_object_id = 0

_cache = None


def _load_cache():
    global _cache
    if _cache is None:
        with open('cache/index.json', 'r') as fp:
            _cache = json.load(fp)
        print('[NICE] Loaded {} entries.  Last run was "{}"'
              .format(len(_cache['entries']), _cache['last_change']))
        _cache['last_change'] = _PREFIX


# TODO: Perfect opportunity for __enter__ and __exit__
def _write_cache():
    # We *could* load the cache here, but calling write_cache indicates an error up the stack
    assert _cache is not None
    with open('cache/index.json.next', 'w') as fp:
        json.dump(_cache, fp, sort_keys=True, indent=0)  # No indent to save some space
    # Hope that os.replace doesn't corrupt the file *and* the git backup.
    os.replace('cache/index.json.next', 'cache/index.json')


def _do_get(url):
    global _last_nice_poll, _object_id
    my_id = _object_id
    _object_id += 1
    print("[NICE] requesting ticket for {} as object #{} …".format(url, my_id))
    now = time.time()
    until = _last_nice_poll + _NICE_WAIT_TIME
    while now < until:
        to_sleep = max(_MIN_SLEEP_TIME, until - now)
        print("[NICE] sleep for {} seconds.".format(to_sleep))
        time.sleep(to_sleep)
        now = time.time()
    print("[NICE] got ticket!  Fetching data …")
    r = requests.get(url)
    name = "object_{}.dat".format(my_id)
    path = os.path.join(_PREFIX, name)
    with open(path, 'wb') as fp:
        fp.write(r.content)
    print("[NICE] done.  Backup saved to {}".format(path))
    # By getting a new timestamp, this gets a bit slower -- by exactly one request.
    _last_nice_poll = time.time()
    return path


def get(url):
    _load_cache()
    path = _cache['entries'].get(url)
    if path is None:
        path = _do_get(url)
        print('[NICE] Adding to cache: ' + url)  # assert that url is a string
        _cache['entries'][url] = path
        _write_cache()
    else:
        print('[NICE] Using cached version of ' + url)
    return path
