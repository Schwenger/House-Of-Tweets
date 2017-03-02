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

    def updateShortpoll(self, username: str, reason: str):
        with self.lock:
            # Write to q somehow
            raise NotImplementedError("Should have implemented this")
