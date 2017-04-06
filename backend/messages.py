#!/usr/bin/env python3

import json
from twitter import UpdatesConsumer
from threading import RLock

msgs_types = {
    "unknown-user": "fail",
    "is-politician": "fail",
    "unknown-bird": "fail",
    "succ-resolved": "info",
    "succ-firstpoll": "succ",
    "del-timeout": "info",
    "del-toomany": "info",
}

with open("messages.json") as msgs_fp_:
    msgs_strings = json.load(msgs_fp_)
    assert msgs_strings.keys() == msgs_types.keys()


def phrase(username: str, reason: str):
    entry = dict()
    entry['twittername'] = username
    entry['reason'] = reason
    entry['status'] = msgs_types[reason]
    assert entry['status'] is not None

    msg_entry = dict()
    entry['message'] = msg_entry
    template = msgs_strings[reason]
    assert template is not None
    for lang in ['de', 'en']:
        msg_entry[lang] = template[lang].format(name=username)

    return entry


class UpdatesQueueAdapter(UpdatesConsumer):
    def __init__(self, q):
        self.lock = RLock()
        self.q = q

    def updateShortpoll(self, username: str, reason: str):
        with self.lock:
            self.q.post(phrase(username, reason))


if __name__ == '__main__':
    import mq
    from time import sleep
    print("Sending some example messages to the real queue:")
    q = UpdatesQueueAdapter(mq.RealQueue("citizenUserFeedbackQueue"))
    for k in sorted(msgs_types.keys()):
        sleep(4)
        user = "Us_%s_er" % k
        print("  Sending a {} message", k)
        q.updateShortpoll(user, k)
    print("All done.")
