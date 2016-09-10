#!/usr/bin/env python3

import mq

from twitterConnection import TwitterConnection
from politicianBackend import PoliticianBackend
from citizenQueueAdapter import CitizenQueueAdapter
from birdBackend import BirdBackend
from citizenBirdQueueAdapter import CitizenBirdQueueAdapter
from twitter import RealTwitterInterface

birdBack = BirdBackend()
polBack = PoliticianBackend()
follow = ["4718199753", "774336282101178368"]
# follow.extend(polBack.getAllTwitteringPoliticians())
print("Configured to follow {} accounts.".format(len(follow)))

queue = mq.Batcher(mq.RealQueue("tweets"))
twi = TwitterConnection(queue, follow, polBack, birdBack, RealTwitterInterface())

c = CitizenQueueAdapter(twi)
c.start()

cbq = CitizenBirdQueueAdapter(polBack)
cbq.start()

print('Backend started ("heeere")')
