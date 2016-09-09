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

all_tests.append(test_mq)


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
