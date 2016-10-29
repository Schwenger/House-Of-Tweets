#!/usr/bin/env python3

import mq
from time import sleep
import vomit  # Aww yiss


def fake_ack():
    q = mq.RealQueue('citizenUserFeedbackQueue')
    q.post(dict(twittername='equu0ae4', birdid='fitis'))
    sleep(3)


def fake_backend():
    vomit.transfer_file('presentation/presentation.json')
    print('Press return to continue with the other part')
    input()
    vomit.transfer_file('presentation/presentation2.json')


if __name__ == '__main__':
    fake_backend()
