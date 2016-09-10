#!/usr/bin/env python3

import mq

from twitterConnection import TwitterConnection
from politicianBackend import PoliticianBackend
from citizenQueueAdapter import CitizenQueueAdapter
from birdBackend import BirdBackend
from citizenBirdQueueAdapter import CitizenBirdQueueAdapter

birdBack = BirdBackend()
polBack = PoliticianBackend()
#follow = ["4718199753"]#["29033470"]
follow = []
follow.extend(polBack.getAllTwitteringPoliticians())
#print(follow)


queue = mq.Batcher(mq.RealQueue("tweets"))

twi = TwitterConnection(queue, follow, polBack, birdBack)

c = CitizenQueueAdapter(twi)
c.start()

cbq = CitizenBirdQueueAdapter(polBack)
cbq.start()

print('Backend started ("heeere")')
