import threading 
import json
import urllib.request
from PIL import Image
from PIL import ImageFile
import os


class PoliticianBackend:
	def __init__(self):
		self.pathToJson = "pols.json"
		self.polList = json.load(open(self.pathToJson))
		self.outPath = "../coffee/modelPoli.coffee"
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
		with self.lock:
			with open(self.pathToJson, 'w') as outfile:
				json.dump(self.polList, outfile, indent=2)
				
			with open(self.outPath, "w") as out:
				out.write("model.politicians= ")
				json.dump(self.polList, out, indent=2)
			os.chdir("..")
			print(os.getcwd())
			os.system("sh compile.sh")
			os.chdir("backend")

	def setCitizensBird(self, tid, bid):
		with self.lock:
			
			if tid in self.polList:
				po = self.polList[str(tid)]
				po["citizen_bird"] = bid
				self.dumpToFile()
