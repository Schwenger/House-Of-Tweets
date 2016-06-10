import pika
import time
import json
from sendingQueueForTweets import *
import os

def getParent( dirr):
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


"""
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.queue_declare(queue='tweets', durable=True)

send = []
send.append(createTestTweet("Christopher", "Hallo ich bin ein Test", "20:55", 0, "red", "groupgreen.png", "amsel-aufgebracht.mp3", "blaumeise-fragend.mp3"))
send.append(createTestTweet("Christopher", "Muuh", "20:56", 0, "red", "groupgreen.png", "amsel-aufgebracht.mp3", "blaumeise-fragend.mp3"))
send.append(createTestTweet("Christopher", "Maah", "20:57", 0, "red", "groupgreen.png", "amsel-aufgebracht.mp3", "blaumeise-fragend.mp3"))
send.append(createTestTweet("Christopher", "Meee", "20:58", 0, "red", "groupgreen.png", "amsel-aufgebracht.mp3", "blaumeise-fragend.mp3"))
send.append(createTestTweet("Christopher", "Miii", "20:59", 0, "red", "groupgreen.png", "amsel-aufgebracht.mp3", "blaumeise-fragend.mp3"))
send.append(createTestTweet("Christopher", "Tztztz", "21:00", 0, "red", "groupgreen.png", "amsel-aufgebracht.mp3", "blaumeise-fragend.mp3"))
send.append(createTestTweet("Christopher", "Aaaaaaaaah", "21:55", 0, "red", "groupgreen.png", "amsel-aufgebracht.mp3", "blaumeise-fragend.mp3"))
send.append(createTestTweet("Christopher", "BBBBB", "21:56", 0, "red", "groupgreen.png", "amsel-aufgebracht.mp3", "blaumeise-fragend.mp3"))
send.append(createTestTweet("Christopher", "CCCCC", "21:57", 0, "red", "groupgreen.png", "amsel-aufgebracht.mp3", "blaumeise-fragend.mp3"))
send.append(createTestTweet("Christopher", "DDDDD", "21:58", 0, "red", "groupgreen.png", "amsel-aufgebracht.mp3", "blaumeise-fragend.mp3"))

for tweet in send:
	print(str([tweet]))
	channel.basic_publish(exchange='',
                      routing_key="tweets",
                      body=json.dumps([tweet]))
	time.sleep(2)
	
"""
