import logging
import os.path
import sys
import time


_logger = None


def _setup():
    # Let's hope this is unique enough
    NAME = "log_%d.txt" % int(time.time() * 1000)
    FILE = os.path.join('log', NAME)
    print('Writing to file: ' + FILE)  # WHITELISTED PRINT

    # create logger with 'spam_application'
    global _logger
    assert _logger is None
    _logger = logging.getLogger('hot')
    _logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(FILE)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    _logger.addHandler(fh)
    _logger.addHandler(ch)

_setup()


# Reduce all the functionality of 'logging' to these few functions,
# since I don't want to care about the rest:
debug = _logger.debug
info = _logger.info
warning = _logger.warning
error = _logger.error

info('Logging started.')  # Self-test


def with_exceptions(run_fn, restart_fn=None, *run_args):
    try:
        run_fn(*run_args)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        error('Unexpected error in {}({}): {}'
              .format(run_fn, run_args, sys.exc_info()[0]))
        if restart_fn is None:
            error('No restart function given.')
        else:
            error('Restarting, but this should have a better handler!')
            restart_fn()
        raise
