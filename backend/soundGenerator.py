import os
import math
from typing import Union
from pydub import *


def get_mood(text: str) -> str:
	questionmarks = text.count('?')
	exclamationmarks = text.count('!')
	multidots = text.count('..')

	exclamationmarks += text.count('?!')
	questionmarks -= text.count('?!')
	# Unwanted side-effect: "Hello!?!?" counts as exclamation, not as question

	caps = len([w for w in text.split() if w.isupper()])

	if caps + exclamationmarks > multidots + questionmarks:
		mood = 'aufgebracht'
	elif caps + exclamationmarks < multidots + questionmarks:
		mood = 'fragend'
	else:
		mood = 'neutral'

	return mood


def get_parent(path):
	return os.path.abspath(os.path.join(path, os.pardir))


HOT_ROOT = get_parent(get_parent(__file__))
SOUND_ROOT = os.path.join(HOT_ROOT, "ext", "sounds")
print("SOUND_ROOT = " + SOUND_ROOT)


# Determine where we *expect* the file, without checking it
def path_raw(bird: str, mood: str, retweet: bool):
	retweet_suffix = "-r" if retweet else ""
	# Goal: "mehlschwalbe-aufgebracht-r.mp3"
	filename = "{bird}-{mood}{suff}.mp3" \
		.format(bird=bird, mood=mood, suff=retweet_suffix)
	return os.path.join(SOUND_ROOT, filename)


# Determine where the result *should* be, without checking it
def path_processed(bird: str, mood: str, retweet: bool, length: int):
	retweet_suffix = "-r" if retweet else ""
	# Goal: "processed/mehlschwalbe-aufgebracht-6000-r.mp3"
	filename = "{bird}-{mood}{suff}-{len}.mp3" \
		.format(bird=bird, mood=mood, len=length, suff=retweet_suffix)
	return os.path.join(SOUND_ROOT, 'processed', filename)


# Determine a viable source/destination pair, such that the
# source exists and the destination is correlated.
# (I.e., the same destination path means you can use caches.)
def find_pair(bird: Union[None, str], mood: str, retweet: bool, length: int):
	if bird is None:
		return None
	candidates = [(bird, mood, retweet),
				  (bird, 'neutral', retweet),
				  ('amsel', 'neutral', False)]
	verbose = False
	for (b, m, r) in candidates:
		candidSource = path_raw(b, m, r)
		if os.path.isfile(candidSource):
			if verbose:
				print("[INFO] Found at {}".format(candidSource))
			return candidSource, path_processed(b, m, r, length)
		else:
			print("[WARN] Source file {} missing, falling back …".format(candidSource))
			verbose = True
	print("[ERR ] All sources and fallbacks missing.  Giving up.")
	return None


# Actual sound conversion and writing.
def createNewSoundfile(src_path, dst_path, length_ms):
	sound = AudioSegment.from_mp3(src_path)
	finDuration_ms = length_ms
	origDuration_ms = math.floor(sound.duration_seconds * 1000)
	if finDuration_ms < origDuration_ms:
		middle_ms = origDuration_ms / 2
		sound = sound[:math.floor(middle_ms + finDuration_ms / 2)]
		sound = sound[-math.floor(finDuration_ms):]
	sound = sound.fade_in(2000).fade_out(2000)
	sound.export(dst_path, format="mp3")


def createOrCached(paths, length_ms):
	if paths is None:
		return
	src_path, dst_path = paths
	if os.path.exists(dst_path):
		print("soundGenerator: using cached file: " + dst_path)
		# no-op
	else:
		print("soundGenerator: creating new file: " + dst_path)
		createNewSoundfile(src_path, dst_path, length_ms)


# There must be a cleverer None-aware approach to this.

def sanitize_bird(b):
	if b is None:
		return None
	return b.replace('ß', 'ss')


def dup(path, idealBid):
	if path is None:
		return None
	return {'natural': path, 'synth': path, 'bid': idealBid}


def get_dst(p):
	if p is None:
		return None
	_, dst = p
	return dst


# Public interface.  Get the conversion rolling, and return a JSON struct with the results.
# The JSON struct is ready for transmission via the 'tweets' queue.
def generate_sound(content: str, retweet: bool, cBird, pBird):
	length_ms = max(len(content) * 250, 10000)
	mood = get_mood(content)
	birds_sanit = [sanitize_bird(cBird), sanitize_bird(pBird)]
	birds_paths = [find_pair(b, mood, retweet, length_ms) for b in birds_sanit]

	for paths in birds_paths:
		createOrCached(paths, length_ms)

	cDst, pDst = [get_dst(p) for p in birds_paths]

	return {'duration': length_ms,
			'citizen': dup(cDst, cBird),
			'poli': dup(pDst, pBird)}
