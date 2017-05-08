BASE_TEMPLATE = '@{handle}: {msg} {link} #HouseOfTweets'

# You MAY use {fromm}, you MUST use {to}
# (The typo in 'fromm' is intentional, as 'from' is a reserved Python-keyword.)
# Must NOT contain
# any opening braces or other formatting instructions.
ACK_TEMPLATES = [
    'Ihre Vogelstimme wurde geändert: {fromm} → {to} 🐦',
    'Okay, Sie haben jetzt eine {to}-Stimme. ☺️',
    'Gerne, eine {to}-Stimme für Sie!',
    '{to}? Kommt sofort! ✔️',
    '{to}? Gute Wahl! 👍'
]

# You MAY use {fromm}, you must NOT use {to}
# (The typo in 'fromm' is intentional, as 'from' is a reserved Python-keyword.)
# Must NOT contain
# any opening braces or other formatting instructions.
NACK_TEMPLATES = [
    'Tweeten Sie Ihre Vogelstimme von dieser Liste:',
    'Das Programm fand keinen Vogelnamen im Tweet. 😞 Liste gefällig?',
    'Keinen Vogelnamen im Tweet gefunden. 🔍 Der Link führt zur Liste:',
    'Wir kennen diese 45 Vogelnamen:',
    'Leider haben wir nicht alle Vogelstimmen, aber hier ist unsere Auswahl:',
]

# https://houseoftweets.github.io/birds.html
ACK_LINK = 'https://t.co/oXBoTZ6VUG'
NACK_LINK = ACK_LINK


def _build_ack(handle, bird_from, bird_to, template):
    # (The typo in 'fromm' is intentional, as 'from' is a reserved Python-keyword.)
    msg = template.format(fromm=bird_from, to=bird_to)
    # Thankfully, the message will never contain
    # any opening braces or other formatting instructions.
    return BASE_TEMPLATE.format(handle=handle, msg=msg, link=ACK_LINK)


def _build_nack(handle, bird_from, template):
    # (The typo in 'fromm' is intentional, as 'from' is a reserved Python-keyword.)
    msg = template.format(fromm=bird_from)
    # Thankfully, the message will never contain
    # any opening braces or other formatting instructions.
    return BASE_TEMPLATE.format(handle=handle, msg=msg, link=NACK_LINK)


NEXT_ACK = 0


def build_some_ack(handle, bird_from, bird_to):
    global NEXT_ACK
    t = ACK_TEMPLATES[NEXT_ACK]
    NEXT_ACK = (NEXT_ACK + 1) % len(ACK_TEMPLATES)
    return _build_ack(handle, bird_from, bird_to, t)


NEXT_NACK = 0


def build_some_nack(handle, bird_from):
    global NEXT_NACK
    t = NACK_TEMPLATES[NEXT_NACK]
    NEXT_NACK = (NEXT_NACK + 1) % len(NACK_TEMPLATES)
    return _build_nack(handle, bird_from, t)


def build_worst_acks():
    handle = 'h' * 15
    bird_from = 'F' * 17
    bird_to = 'T' * 17
    return [_build_ack(handle, bird_from, bird_to, template)
            for template in ACK_TEMPLATES]


def build_worst_nacks():
    handle = 'h' * 15
    bird_from = 'F' * 17
    return [_build_nack(handle, bird_from, template)
            for template in NACK_TEMPLATES]
