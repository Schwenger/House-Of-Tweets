#!/bin/bash
# Provide minimal working "environment" (sound dir) for the backend.
# Contains bachisms.

set -e


# == Are we even in the correct directory? ==

if [ ! -r 'README.md' ]
then
    echo 'No README.md found.'
    echo 'pwd =' `pwd`
    echo 'Script should be called from project root.'
    exit 1
fi
ACTUAL=$(head -n 2 README.md)
EXPECT=$'House of Tweets\n==============='
if [ "${EXPECT}" != "${ACTUAL}" ]
then
    echo 'Wrong README.md found.'
    echo "Actual header was:"
    echo "${ACTUAL}"
    echo 'pwd =' `pwd`
    echo 'Script should be called from project root.'
    exit 2
fi


# == Actually replace it ==

echo "Old ext/sounds link: " $(file ext/sounds)
ln -sf ../tools/minimal_sound/sounds ext/
echo "New ext/sounds link: " $(file ext/sounds)
