#!/bin/bash
# Self-made updater script.  Needs bash.

# Insert something like this into your USER'S crontab:
#     21 * * * * /home/user/bin/dns-update-https.sh xxxxxxxxxxxxxxxxxxxxxxxx mydomain
# Where xxxxxxxxxxxxxxxxxxxxxxxx is the "dynamic v2" token for your domain.
# See https://freedns.afraid.org/dynamic/v2/

set -e

UPDATESTR=$(wget -q -O - "https://sync.afraid.org/u/$1/")
case "$UPDATESTR" in
    No\ IP\ change\ detected*)
        # No output
        ;;
    *)
        echo "IP update possibly failed for domain '$2':"
        echo "$UPDATESTR"
        ;;
esac
