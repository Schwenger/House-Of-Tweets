import os
import requests
import threading
import time

# Amount of seconds to wait between each download.
_NICE_WAIT_TIME = 3
# Minimal sleep time for grace, in seconds.
_MIN_SLEEP_TIME = 0.1

# Let's hope this is unique enough
_PREFIX = "results_" + str(int(time.time() * 1000))
os.mkdir(_PREFIX)
print("Wrapping everything in " + _PREFIX)


_last_nice_poll = 0

_object_id = 0


def _unlocked_get(url):
    global _last_nice_poll, _object_id
    my_id = _object_id
    _object_id += 1
    print("get_nice: requesting ticket for {} as object #{} …".format(url, my_id))
    now = time.time()
    until = _last_nice_poll + _NICE_WAIT_TIME
    while now < until:
        to_sleep = max(_MIN_SLEEP_TIME, until - now)
        print("waiting: sleep for {} seconds.".format(to_sleep))
        time.sleep(to_sleep)
        now = time.time()
    print("get_nice: got ticket!  Fetching data …")
    r = requests.get(url)
    name = "object_{}.dat".format(my_id)
    path = os.path.abspath(os.path.join(_PREFIX, name))
    with open(path, 'wb') as fp:
        fp.write(r.content)
    print("get_nice: done.  Backup saved to {}".format(path))
    # By getting a new timestamp, this gets a bit slower -- by exactly one request.
    _last_nice_poll = time.time()
    return path


# Locking.  Just in case the crawler gets much more complicated than we thought.
_poll_lock = threading.RLock()


def get(url):
    with _poll_lock:
        return _unlocked_get(url)
