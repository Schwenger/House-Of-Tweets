import json
import mylog


def _simplify(s):
	return s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss").strip()


class BirdBackend:
	def __init__(self):
		with open("birds.json", 'r') as fp:
			self.bJson = json.load(fp)
		self.keyword2bid = dict()

		for bid, bird in self.bJson.items():
			# TODO: find a way to resolve English names
			# self._update(bird['en_name'], bid)  # English name are multi-word!
			self._update(bird['de_name'], bid)

	def _update(self, name, bid):
		simple_name = _simplify(name)
		assert ' ' not in simple_name  # Otherwise, name parsing won't work.
		assert simple_name not in self.keyword2bid
		self.keyword2bid[simple_name] = bid

	# Always returns a string.  If everything goes wrong, it lies.
	def getName(self, bid):
		b = self.bJson.get(bid)
		if b is None:
			mylog.error('Tried to resolve invalid Bird-ID "{}",'
				        ' will go with "Goldammer" instead'.format(bid))
			return 'Goldammer'
		return b['de_name']

	def getBid(self, name):
		return self.keyword2bid.get(_simplify(name))
