import threading 
import json
import urllib.request
from PIL import Image
from PIL import ImageFile
import os


class PolitianBackend:
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
		
	def getAllPolitians(self):
		return self.polList
		
	def createPolitian(self, pid, name, party, twittering, self_bird, citizen_bird, cv, images):
		dic = {}
		#dic["id"] = pid
		dic["name"] = name 
		dic["party"] = party
		dic["twittering"] = twittering
		dic["self_bird"] = self_bird
		dic["citizen_bird"] = citizen_bird
		dic["cv"] = cv
		
		im = None
		if images is not None:
			if "http:" not in images and "https:" not in images:
				images = "http://" + images
				
			print("images = " + images)
			fullfilename = os.path.join("../ext/images/politicians/", pid + ".jpg")
			urllib.request.urlretrieve(images, fullfilename)
			self.cutImage(fullfilename, fullfilename, (500,500))
			thumb = os.path.join("../ext/images/politicians/", "t" +pid + ".jpg")
			self.cutImage(fullfilename, thumb, (75,75))
			
			im = {}
			im["pathToThumb"] = pid + ".jpg"
			im["pathToImage"] = "t" + pid + ".jpg"
			
		dic["images"] = im
		
		return (pid, dic)

	def getAllTwitteringPolitians(self):
		res = []
		with self.lock:
			for i in self.polList:
				p = self.polList[str(i)]
				if p["twittering"] is not None:
					res.append(str(p["twittering"]["twitterId"]))
				
		return res
		
	def addPolitian(self, pid, name, party, twittering, self_bird, citizen_bird, cv, images):
		# check for dupicates ...
		
		with self.lock:
			(pid, dic) = self.createPolitian(pid, name, party, twittering, self_bird, citizen_bird, cv, images)
			
			if pid in self.polList:
				return False
			
			self.polList[pid] = dic
			#print(self.polList)			
			self.dumpToFile()
			return True
			
	def delPolitian(self, pid):
		#TODO delte politian
		toDel = []
		with self.lock:
			if str(pid) in self.polList:
				del self.polList[str(pid)]
				self.dumpToFile()
				return True
			else:
				return False
				
			
			
	def getPolitian(self, tid):
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
		
	
	def setPolitiansBird(self, tid, bid):
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
		#print(self.polList)
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
			
			

"""			
pb = PolitianBackend()
#dic["self_bird"] = self_bird
#dic["citizen_bird"] = citizen_bird
m = {"ä" : "ae" , "ö":"oe", "ü":"ue", "ß":"ss"}
alll=pb.getAllPolitians() 
for i in range(0, len(alll)):
	p = alll[str(i)]
	for k,v in m.items():
		if k in p["citizen_bird"]:
			p["citizen_bird"] = p["citizen_bird"].replace(k,v)
			
		if k in p["self_bird"]:
			p["self_bird"] = p["self_bird"].replace(k,v)
		
pb.dumpToFile()	
"""

