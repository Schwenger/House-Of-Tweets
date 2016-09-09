#!/usr/bin/env python3

from soundGenerator import SoundGenerator

tweetId = 1
content = "a"
isRetweet = True
# politician = self.pb.getPolitician(status["user"]["id"])
cBird = "weisskopfseeadler"
pBird = "eichelhaeher"
gen = SoundGenerator()
(pPath, cPath) = gen.makeSounds(tweetId, content, isRetweet, cBird, pBird)

print(pPath + " und  " + cPath)
