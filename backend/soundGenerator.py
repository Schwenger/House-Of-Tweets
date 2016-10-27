import os
import math
import mylog
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
mylog.info("SOUND_ROOT = " + SOUND_ROOT)


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
	filename = "{bird}-{mood}{suff}-{len}_v2.mp3" \
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
				  (bird, 'fragend', retweet),
				  (bird, 'aufgebracht', retweet),
				  ('amsel', 'neutral', False)]
	verbose = False
	for (b, m, r) in candidates:
		candidSource = path_raw(b, m, r)
		if os.path.isfile(candidSource):
			if verbose:
				mylog.info("Found at {}".format(candidSource))
			return candidSource, path_processed(b, m, r, length)
		else:
			mylog.warning("Source file {} missing, falling back ...".format(candidSource))
			verbose = True
	mylog.error("All sources and fallbacks missing.  Giving up.")
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
	else:
		finDuration_ms = origDuration_ms
	sound = sound.fade_in(2000).fade_out(2000)
	sound.export(dst_path, format="mp3")
	return finDuration_ms


def createOrCached(src_path, dst_path, length_ms):
	if os.path.exists(dst_path):
		mylog.info("soundGenerator: using cached file: " + dst_path)
		# no-op
		return length_ms
	else:
		mylog.info("soundGenerator: creating new file: " + dst_path)
		return createNewSoundfile(src_path, dst_path, length_ms)


def gen_bird(bird, mood, retweet, length_ms):
	use_bird = bird.replace('ß', 'ss')  # TODO: Still needed?
	path_src, path_dst = find_pair(use_bird, mood, retweet, length_ms)
	real_ms = createOrCached(path_src, path_dst, length_ms)
	return {'natural': path_dst, 'bid': bird, 'duration': real_ms}


# Public interface.  Get the conversion rolling, and return a JSON struct with the results.
# The JSON struct is ready for transmission via the 'tweets' queue.
def generate_sound(content: str, retweet: bool, cBird, pBird):
	length_ms = max(len(content) * 250, 10000)
	mood = get_mood(content)

	ret = {'citizen': gen_bird(cBird, mood, retweet, length_ms)}
	if pBird is not None:
		ret['poli'] = gen_bird(pBird, mood, retweet, length_ms)
	return ret
