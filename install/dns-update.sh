#!/bin/sh

# FreeDNS updater script
# Insert something like this into your USER'S crontab:
#     21 * * * * dns-update.sh
# Where you should use a new random minute for each host, like this:
#     $ python3 -c $'import random\nprint(random.choice(range(60)))'

set -e

DNSPASSWORD=im_sorry  # FIXME
SUBDUMOAIN=tweetianX  # FIXME

UPDATEURL="http://freedns.afraid.org/dynamic/update.php?${DNSPASSWORD}"
DOMAIN="${SUBDOMAIN}.privatedns.org"
registered=$(nslookup $DOMAIN|tail -n2|grep A|sed s/[^0-9.]//g)
current=$(wget -q -O - http://checkip.dyndns.org|sed s/[^0-9.]//g)
if [ "$current" != "$registered" ]
then
  wget -q -O /dev/null $UPDATEURL
  echo "DNS(${SUBDOMAIN}) updated from ${registered} to ${current} on:"
  date
fi
