import threading 
import json

_SKIP_WRITEBACK = False


def set_skip_writeback(to: bool):
	global _SKIP_WRITEBACK
	_SKIP_WRITEBACK = to
	print("politicianBackend: UPDATE SKIP_WRITEBACK = {}".format(_SKIP_WRITEBACK))


def check_writeback():
	print("politicianBackend: SKIP_WRITEBACK is currently {}".format(_SKIP_WRITEBACK))


BACKEND_POLI_DB = 'pols.json'
FRONTEND_POLI_DB = '../coffee/model/model_polis.coffee'


class PoliticianBackend:
	def __init__(self):
		self.poliList = json.load(open(BACKEND_POLI_DB))
		self.lock = threading.RLock()

		self.polByPid = dict()
		for poli in self.poliList:
			self.polByPid[poli["pid"]] = poli

		# This references the same politician dicts, just like pointers.
		# In other words: updates will always be reflected in both lookup tables.
		self.polByTid = dict()
		for poli in self.poliList:
			if poli["twittering"] is None:
				continue
			self.polByTid[str(poli["twittering"]["twitterId"])] = poli

		print("Loaded {} polititians; {} of them have a TID, {} have a PID"
			  .format(len(self.poliList), len(self.polByTid), len(self.polByPid)))

	def getAllTwitteringPoliticians(self):
		with self.lock:
			# Copy the keys, just in case.
			return set(self.polByTid.keys())

	def getPolitician(self, tid):
		tid = str(tid)
		try:
			with self.lock:
				# Copy the politician, in case a concurrent
				# setPoliticianBird comes in.
				return dict(self.polByTid[tid])
		except KeyError:
			print("ERROR: Tried to get non-existent politician {}".format(tid))
			return None

	def setBird(self, tid, bid, actor):
		assert actor in ['p', 'c']
		bird_key = 'self_bird' if actor == 'p' else 'citizen_bird'
		tid = str(tid)
		with self.lock:
			try:
				# Copy the politician, in case a concurrent
				# setPoliticianBird comes in.
				poli = self.polByTid[tid]
			except KeyError:
				print("ERROR: Tried to update non-existent politician {tid}"
					  " to bird {bid}, actor={actor}"
					  .format(tid=tid, bid=bid, actor=actor))
				return
			poli[bird_key] = bid
			self.__dumpToFile()

	def __dumpToFile(self):
		if _SKIP_WRITEBACK:
			print("=" * 77)
			print("politicianBackend: skipping write-back <THIS SHOULD NOT HAPPEN IN PRODUCTION>")
			print("=" * 77)
			return

		with open(BACKEND_POLI_DB, 'w') as outfile:
			json.dump(self.poliList, outfile, indent=2)

		with open(FRONTEND_POLI_DB, "w") as out:
			out.write("@politicians:")
			json.dump(self.polByPid, out, indent=2)
