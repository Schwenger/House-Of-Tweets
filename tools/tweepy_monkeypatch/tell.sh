#!/bin/sh

# This file is written to be executable by a human, in the worst case.

# Setup
set -e
PYTH=false
if command -v python3 > /dev/null 2> /dev/null
then
    PYTH=python3
elif command -v python > /dev/null 2> /dev/null
then
    PYTH=python
else
    echo "Can't find python o.O"
    exit 1
fi
MYBEFORE=tools/tweepy_monkeypatch/before
MYAFTER=tools/tweepy_monkeypatch/after

# Find path to culprit file
STRPY=$($PYTH -c 'import tweepy; print(tweepy.streaming.__file__)')
# Most the time, this executes:
# python3 -c 'import tweepy; print(tweepy.streaming.__file__)
# Should be something like /usr/lib/python3/dist-packages/tweepy/streaming.py

# Sanity checks
# Could be done in a loop, but I'm too lazy to do that safely (spaces in filenames!)
if [ ! -r "$STRPY" ]
then
    echo "# Can't read file at '$STRPY'"
    exit 1
fi
if [ ! -r "$MYBEFORE" ]
then
    echo "# Can't read file at '$MYBEFORE'"
    exit 1
fi
if [ ! -r "$MYAFTER" ]
then
    echo "# Can't read file at '$MYAFTER'"
    exit 1
fi

# Evaluate situation
# Any errors might be interesting, so don't swallow stderr
if diff "$STRPY" "$MYAFTER" > /dev/null
then
    if diff "$STRPY" "$MYBEFORE" > /dev/null
    then
        echo "# Unknown version of that file is installed.  Good luck, giving up."
        exit 1
    else
        echo "# Patched version installed, no action needed."
        exit 0
    fi
else
    if ! diff "$STRPY" "$MYBEFORE" > /dev/null
    then
        echo "# Dafuq?  $MYBEFORE and $MYAFTER should be different, but aren't?!"
        exit 1
    else
        echo "# Unpatched 'before' version installed.  Execute this:"
        echo "sudo cp '$MYAFTER' '$STRPY'"
        echo "# Failing to show you this message."
        exit 2
    fi
fi
