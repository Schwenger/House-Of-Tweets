import os
import math
import time

from pydub import *

# Let's hope that the backend doesn't get started twice within a second
STARTUP = str(int(time.time() * 1000))

processed_tweets = 0


class SoundGenerator:
	def __init__(self):
		self.soundDir = self.getSoundDir()

	### tweet parsing ####

	def parseTweet(self, content):
		caps = 0 	#counts words in CAPS-LOCK
		qm = 0		#counts questionmarks
		em = 0		#counts exclamationmarks
		dot = 0		#counts multiple dots
		mood = None	#neutral or aufgebracht or fragend
		text = content

		qm += text.count('?')
		em += text.count('?!')
		qm -= text.count('?!')
		em += text.count('!')
		dot += text.count('..')

		words = text.split()

		for w in words:
			if w.isupper():
				caps += 1

		if caps + em > dot + qm:
			mood = 'aufgebracht'
		elif caps + em < dot + qm:
			mood = 'fragend'
		else:
			mood = 'neutral'

		return mood


	### directories and files ###	

	def getParent(self, dirr):
		return os.path.abspath(os.path.join(dirr, os.pardir))

	def getSoundDir(self):
		extSounds = os.path.sep + "ext" + os.path.sep + "sounds"
		hotRoot = self.getParent(__file__)
		return os.path.abspath(os.path.join(hotRoot, os.pardir)) + extSounds

	def getFileName(self, bird, mood, retweet):
		if retweet == False:
			return str(bird) + "-" + mood + ".mp3"
		else:
			return str(bird) + "-" + mood + "-r.mp3"

	def getSoundPath(self, bird, mood, retweet):
		return self.soundDir + os.path.sep + self.getFileName(bird, mood, retweet)

	def soundExists(self, bird, mood, retweet):
		print("SoundExists " + self.getSoundPath(bird, mood, retweet) + "   " + str(os.path.isfile(self.getSoundPath(bird, mood, retweet))))
		return os.path.isfile(self.getSoundPath(bird, mood, retweet))


	### sound handling ###

	def makeSounds(self, tweetid, content, isRetweet, cBird, pBird):
		mood = self.parseTweet(content)

		if pBird is not None:
			pMood = self.getClosestMood(pBird, mood, isRetweet)
		
		cMood = self.getClosestMood(cBird, mood, isRetweet)

		if pBird is not None:
			pPath = self.getSoundPath(pBird, pMood, isRetweet)
		cPath = self.getSoundPath(cBird, cMood, isRetweet)

		pRes = None
		pdur = 0
		if pBird is not None:
			(pRes, pdur) = self.createNewSoundfile(pBird, pMood, isRetweet, len(content), tweetid, 'p')
		
		(cRes, cdur) = self.createNewSoundfile(cBird, cMood, isRetweet, len(content), tweetid, 'c')

		return(pRes, cRes, pdur, cdur)

	def getClosestMood(self, bird, mood, retweet):
		n = 'neutral'
		a = 'aufgebracht'
		f = 'fragend'
		nExists = self.soundExists(bird, n, retweet)
		aExists = self.soundExists(bird, a, retweet)
		fExists = self.soundExists(bird, f, retweet)

		err = "No suitable sound file for " + bird + " found."
		
		if self.soundExists(bird, mood, retweet):
			return mood
		elif mood == 'neutral':
			if fExists:
				return f
			elif aExists:
				return a
			else:
				print(err)
		elif mood == 'aufgebracht':
			if nExists:
				return n
			elif fExists:
				return f
			else:
				print(err)
		elif mood == 'fragend':
			if nExists:
				return n
			elif aExists:
				return a
			else:
				print(err)
		else:
			print(mood + "is not an accepted mood. Accepted moods are: neutral, aufgebracht, fragend")

	def createNewSoundfile(self, bird, mood, retweet, length, tweetid, group):
		finDuration = max(length * 250, 6000)
		sound = AudioSegment.from_mp3(self.getSoundPath(bird, mood, retweet))
		origDuration = math.floor(sound.duration_seconds)*1000
		print("original: " + str(origDuration))
		print("final: " + str(finDuration))
		print(str(finDuration > origDuration))
		if finDuration < origDuration:
			middle = math.floor(origDuration/2)
			print("middle: " + str(middle))
			print("first length: " + str(middle + math.floor(finDuration/2)))
			sound = sound[:(middle + math.floor(finDuration/2))]
			sound = sound[-math.floor(finDuration):]
		sound = sound.fade_in(2000).fade_out(2000)
		global processed_tweets
		path = self.soundDir + os.path.sep + "processed/" + STARTUP + "_" + str(processed_tweets) + ".mp3"
		processed_tweets += 1
		sound.export(path, format="mp3")
		return (path, finDuration)


def generate_sound(content: str, retweet: bool, birds):
	# Why is that even a class?  FIXME: dissolve 'SoundGenerator' into functions
	sg = SoundGenerator()
	cBird, pBird = birds
	return sg.makeSounds(STARTUP, content, retweet, cBird, pBird)
"""
- `sound`: JSON object
    - `duration`: integer, length, in milliseconds, of the sounds
    - `citizen`: JSON object, describing the bird chosen by the citizen
        - `natural`: string, valid path to the bird's natural sound, e.g. `"/home/eispin/workspace/House-Of-Tweets/ext/sounds/processed/774316458742583296r-c_n.mp3"`
        - `synth`: string, valid path to the bird's "synthesized" sound or "artistic interpretation", e.g. `"/home/eispin/workspace/House-Of-Tweets/ext/sounds/processed/774316458742583296r-c_s.mp3"`
    - `poli`: same, but chosen by the politician.  If not a politician, `null`.
"""
