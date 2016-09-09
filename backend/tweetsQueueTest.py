from sendingQueueForTweets import *
import os


def getParent(dirr):
	return os.path.abspath(os.path.join(dirr, os.pardir))


def getSoundDir():
	extSounds = os.path.sep + "ext" + os.path.sep + "sounds"
	hotRoot = getParent(__file__)
	return os.path.abspath(os.path.join(hotRoot, os.pardir)) + extSounds

	
def createTestTweet(name, twittername, byPoli, content, time, tid, partycolor, image, soundc, soundp, retweeted):
		d = {}
		d["name"] = name
		d["twitterName"] = twittername
		d["byPoli"] = byPoli
		d["content"] = content
		d["time"] = time
		d["id"] = tid
		d["partycolor"] = partycolor
		d["image"] = image
		d["soundc"] = soundc
		d["soundp"] = soundp
		d["retweet"] = retweeted
		return d
	
	
q = SendingQueueForTweets()		
#q.addTweet(createTestTweet("Christopher", "Hallo ich bin ein Test", "20:55", 0, "red", "groupgreen.png", "amsel-aufgebracht.mp3", "blaumeise-fragend.mp3", True))
#							name,         twittername, byPoli, content,               time,      tid,  partycolor, image,                                                                   soundc,                       soundp,           retweeted
q.addTweet(createTestTweet("Christopher", "pes04",      True, "Ich bin ein Test!!!", "1453840647", 0,  "red",      "https://pbs.twimg.com/profile_images/573488117560295424/5qsXbC5W.jpeg", getSoundDir() + "/amsel-aufgebracht.mp3", getSoundDir() +"/blaumeise-fragend.mp3", False))
