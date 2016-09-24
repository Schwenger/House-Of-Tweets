#!/usr/bin/env python3

import fileinput
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
		self.polByPid = json.load(open(BACKEND_POLI_DB))
		self.lock = threading.RLock()

		# This references the same politician dicts, just like pointers.
		# In other words: updates will always be reflected in both lookup tables.
		self.polByTid = dict()
		#for poli in self.polByPid:
		#	assert "twittering" in poli, poli['pid']
		#	self.polByTid[str(poli["twittering"]["twitterId"])] = poli

		print("Loaded {} polititians; {} of them have a TID"
			  .format(len(self.polByPid), len(self.polByTid)))

	def getAllTwitteringPoliticians(self):
		with self.lock:
			# Copy the keys, just in case.
			return set(self.polByTid.keys())

	# Returns 'None' if not a politician
	def getPolitician(self, tid):
		tid = str(tid)
		try:
			with self.lock:
				# Copy the politician, in case a concurrent
				# setPoliticianBird comes in.
				return dict(self.polByTid[tid])
		except KeyError:
			return None

	def setBird(self, pid, bid, actor):
		assert actor in ['p', 'c']
		bird_key = 'self_bird' if actor == 'p' else 'citizen_bird'
		with self.lock:
			try:
				# Copy the politician, in case a concurrent
				# setPoliticianBird comes in.
				poli = self.polByPid[pid]
			except KeyError:
				print("ERROR: Tried to update non-existent politician {pid}"
					  " to bird {bid}, actor={actor}"
					  .format(pid=pid, bid=bid, actor=actor))
				return
			poli[bird_key] = bid
			self._dumpToFile()

	def _dumpToFile(self):
		if _SKIP_WRITEBACK:
			print("=" * 77)
			print("politicianBackend: skipping write-back <THIS SHOULD NOT HAPPEN IN PRODUCTION>")
			print("=" * 77)
			return

		with open(BACKEND_POLI_DB, 'w') as outfile:
			json.dump(self.polByPid, outfile, sort_keys=True, indent=2)

		with open(FRONTEND_POLI_DB, "w") as out:
			out.write("@politicians = ")
			json.dump(self.polByPid, out, sort_keys=True, indent="\t")
		for line in fileinput.input([FRONTEND_POLI_DB], inplace=True):
			print('\t' + line.rstrip('\n'))


# Use this if you need to make some processing / regeneration.
def poli_modify():
	check_writeback()
	set_skip_writeback(False)
	check_writeback()
	print("Fiddling with politicianBackend.")
	pb = PoliticianBackend()

	# Do your thing here, e.g.:
	#     pB.setBird('395912134', 'fitis', 'c')
	#     # This is a no-op on the original pols.json
	# Or to purge everything French:
	#     for poli in pb.poliList:
	#         cv = poli['cv']
	#         if 'fr' in cv:
	#             print('Purged the French out of ' + poli['name'])
	#             del cv['fr']

	import time, twitter
	tw = twitter.RealTwitterInterface()
	for poli in pb.polByPid.values():
		account = poli['twittering']
		if 'twitterId' not in account:
			print('Resolving ' + poli['name'])
			time.sleep(2)
			account['twitterId'] = tw.resolve_name(account['twitterUserName'])

	# Note:
	# - setBird automatically calls dumpToFile.
	#   In all other cases, you'll need to call __dumpToFile by hand, like this:
	pb._dumpToFile()

	print("Now check by hand.")


if __name__ == '__main__':
	print("Are you sure you want to rewrite pols.json?")
	print("Uncomment me, I'm not gonna let ya!")
	# Uncomment to run:
	# poli_modify()
