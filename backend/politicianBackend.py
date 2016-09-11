import threading 
import json
import urllib.request
import fileinput
from PIL import Image
from PIL import ImageFile
import os

_SKIP_WRITEBACK = False


def set_skip_writeback(to: bool):
	global _SKIP_WRITEBACK
	_SKIP_WRITEBACK = to
	print("politicianBackend: UPDATE SKIP_WRITEBACK = {}".format(_SKIP_WRITEBACK))


def check_writeback():
	print("politicianBackend: SKIP_WRITEBACK is currently {}".format(_SKIP_WRITEBACK))


class PoliticianBackend:
	def __init__(self):
		self.pathToJson = "pols.json"
		self.polList = json.load(open(self.pathToJson))
		self.outPath = "../coffee/model/model_polis.coffee"
		self.lock = threading.RLock()
		
	def cutImage(self, path, out, size):
		ImageFile.LOAD_TRUNCATED_IMAGES = True
		im = Image.open(path)
		im.thumbnail(size)
		im.save(out, "JPEG")
		
	def getAllPoliticians(self):
		return self.polList

	def getAllTwitteringPoliticians(self):
		res = []
		with self.lock:
			for i in self.polList:
				p = self.polList[str(i)]
				if p["twittering"] is not None:
					res.append(str(p["twittering"]["twitterId"]))
				
		return res

	def getPolitician(self, tid):
		ret = None
		with self.lock:
			for p in self.polList:
				po = self.polList[str(p)]
				#print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
				#print(po)

				if po["twittering"] is None:
					continue
				
				if str(po["twittering"]["twitterId"]) == str(tid):
					ret = po
					break
			
		print("Ret is None " + str(ret is None))
		return ret

	def setPoliticiansBird(self, tid, bid):
		with self.lock:
			for p in self.polList:
				po = self.polList[str(p)]

				if po["twittering"] is None:
					continue
				
				if po["twittering"]["twitterId"] == str(tid):
					print("!!!!!!!!!!!!!!!! before " + str(po["citizen_bird"]))
					po["self_bird"] = bid
					print("!!!!!!!!!!!!!!!! set to " + str(bid))
					self.dumpToFile()
					return p

	def dumpToFile(self):
		if _SKIP_WRITEBACK:
			print("=" * 77)
			print("politicianBackend: skipping write-back <THIS SHOULD NOT HAPPEN IN PRODUCTION>")
			print("=" * 77)
			return

		with self.lock:
			with open(self.pathToJson, 'w') as outfile:
				json.dump(self.polList, outfile, indent=2)
				
			with open(self.outPath, "w") as out:
				out.write("@politicians = ")
				json.dump(self.polList, out, indent="\t")
			for line in fileinput.input([self.outPath], inplace=True):
				print('\t' + line.rstrip('\n'))

	def setCitizensBird(self, tid, bid):
		with self.lock:
			
			if tid in self.polList:
				po = self.polList[str(tid)]
				po["citizen_bird"] = bid
				self.dumpToFile()

b = PoliticianBackend()
b.dumpToFile()