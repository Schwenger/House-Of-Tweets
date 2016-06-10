import os
import math
from pydub import *

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

	'''def changeBird(self, tweet, birds, path):
		f = open(path, 'r+')
		politician = tweet.image.replace('.jpg', '')
		text = tweet.content
		text = text.replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe')
		text = text.replace('Ä', 'ae').replace('Ü', 'ue').replace('Ö', 'oe')
		text = text.replace('ß', 'ss').lower()
		words = text.split()

		for w in words:
			if w in birds:
				rightSection = False
				rightPolitician = False
				for line in f:
					rightSection = rightSection or "politicians: {" in line
					rightPolitician = rightPolitician or '"' + politician + '": {' in line
					if rightSection and rightPolitician and "self_bird:" in line:
						parts = line.split('"')
						line.replace(parts[1], w)
	'''


	### directories and files ###	

	def getParent(self, dirr):
		return os.path.abspath(os.path.join(dirr, os.pardir))

	def getSoundDir(self):
		extSounds = os.path.sep + "ext" + os.path.sep + "sounds"
		hotRoot = self.getParent(self.getParent(__file__))
		return os.path.abspath(os.path.join(hotRoot, os.pardir)) + extSounds

	def getFileName(self, bird, mood, retweet):
		if retweet == False:
			return bird + "-" + mood + ".mp3"
		else:
			return bird + "-" + mood + "-r.mp3"

	def getSoundPath(self, bird, mood, retweet):
		return self.soundDir + os.path.sep + self.getFileName(bird, mood, retweet)

	def soundExists(self, bird, mood, retweet):
		return os.path.isfile(self.getSoundPath(bird, mood, retweet))


	### sound handling ###

	def makeSounds(self, tweetid, content, isRetweet, cBird, pBird):
		mood = parseTweet(content)

		pMood = self.getClosestMood(cBird, mood, isRetweet)
		cMood = self.getClosestMood(cBird, mood, isRetweet)

		pPath = getSoundPath(pBird, pMood, isRetweet)
		cPath = getSoundPath(cBird, cMood, isRetweet)

		pRes = createNewSoundfile(pBird, pMood, isRetweet, len(content), tweetid, 'p')
		cRes = createNewSoundfile(cBird, cMood, isRetweet, len(content), tweetid, 'c')

		return(pRes, cRes)

	def getClosestMood(self, bird, mood, retweet):
		wantedSound = self.getFileName(bird, mood, retweet)

		n = 'neutral'
		a = 'aufgebracht'
		f = 'fragend'
		nExists = self.soundExists(bird, n, retweet)
		aExists = self.soundExists(bird, a, retweet)
		fExists = self.soundExists(bird, f, retweet)

		err = "No suitable sound file for " + bird + " found."
		
		if self.soundExists(wantedSound):
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
		path = self.soundDir + os.path.sep + "processed/" + str(tweetid) + group + ".mp3"
		sound.export(path, format="mp3")
		return path
