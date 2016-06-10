from soundGenerator import SoundGenerator
	
	
	
tweetId = 1
content = "a"
isRetweet = True
#politian = self.pb.getPolitian(status["user"]["id"])
cBird = "weisskopfseeadler"
pBird = "eichelhaeher"
gen = SoundGenerator()
(pPath, cPath) = gen.makeSounds(tweetId, content, isRetweet, cBird, pBird)

print(pPath + " und  " + cPath)
