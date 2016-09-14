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
follow = polBack.getAllTwitteringPoliticians()
print("Configured to follow {} accounts.".format(len(follow)))

queue = mq.Batcher(mq.RealQueue("tweets"))
twi = TwitterConnection(queue, follow, polBack, birdBack, RealTwitterInterface())

c = CitizenQueueAdapter(twi, mq.RealQueue("userBirdNack"))
c.start()

cbq = CitizenBirdQueueAdapter(polBack)
cbq.start()

print('Backend started ("heeere")')
