#!/usr/bin/env python3

import mq

all_tests = []
MANUAL_TESTS = False


def test_mq():
    def run_with(maker):
        conn = maker("test_mq")
        conn.post("My lovely message")
    print("Testing mq.PrintQueue:")
    run_with(mq.PrintQueue.new)
    if MANUAL_TESTS:
        print("Testing mq.RealQueue. MANUAL: http://localhost:15672/#/queues/%2F/test_mq")
        run_with(mq.RealQueue.new)
    else:
        print("SKIP RealQueue access")

all_tests.append(test_mq)


def test_batching_x(n, batch):
    import time
    # from datetime import datetime
    print("Testing batching.TweetBatcher:")
    conn = mq.PrintQueue.new('test_batching')
    batcher = mq.Batcher(conn)
    # argument should be a tweet, but who cares
    for i in range(n):
        batcher.add("Should be batch {batch}, message {i}/{n}"
                    .format(batch=batch, i=i, n=n))
    time.sleep(mq.BATCH_TIMEOUT / 2.0)
    assert conn.received == 0
    time.sleep(mq.BATCH_TIMEOUT)
    assert conn.received == 1


def test_batching1():
    test_batching_x(1, 1)

all_tests.append(test_batching1)


def test_batching7():
    test_batching_x(7, 2)

all_tests.append(test_batching7)


def test_all():
    # This might show weird behavior if you modify MANUAL_TESTS by hand
    print('[TEST] -- Running all tests (MANUAL_TESTS={}) --'.
          format(MANUAL_TESTS))
    for t in all_tests:
        print("[TEST] {}".format(t))
        t()
        print("[DONE] {}".format(t))
    print('[DONE] -- Done with all tests --')

if __name__ == '__main__':
    test_all()
