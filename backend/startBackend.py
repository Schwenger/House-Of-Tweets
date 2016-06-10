from sendingQueueForTweets import SendingQueueForTweets
from twitterConnection import TwitterConnection
from tweepy.auth import OAuthHandler
from politianBackend import PolitianBackend
from citizenQueueAdapter import CitizenQueueAdapter
from persistQueueAdapter import PersistQueueAdapter
from birdBackend import BirdBackend
from citizenBirdQueueAdapter import CitizenBirdQueueAdapter

birdBack = BirdBackend()
polBack = PolitianBackend()
#follow = ["4718199753"]#["29033470"]
follow = []
follow.extend(polBack.getAllTwitteringPolitians())




#print(follow)



queue = SendingQueueForTweets()

twi = TwitterConnection(queue, follow, polBack, birdBack)


c = CitizenQueueAdapter(twi)
c.start()

pqa = PersistQueueAdapter(polBack, twi)
pqa.start()

cbq = CitizenBirdQueueAdapter(polBack)
cbq.start()
print("heeere")


