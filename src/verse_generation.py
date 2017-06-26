import random
import pickle
import time
from verse_pattern_tools import is_rhyme

PUNCTUATION = "’()[]\{\}<>:,…!.«»?‘’“”;/⁄␠·&@*\\•^¤¢$€£¥₩₪†‡°¡¿¬#№%‰‱¶′§~¨_|¦⁂☞∴‽※"

class VerseGenerator(object):
	
	def __init__(self, filename, soundsFile):
		self.filename = filename
		self.soundsFile = soundsFile
		self.cache = pickle.load(open(self.filename, 'rb'))	
		self.sounds = pickle.load(open(self.soundsFile, 'rb'))	

	def __transform_to_rhythm(self, line):
		rhythm = ''
		for char in line:
			if char in 'ЁУЕЫАОЭЯИЮёуеыаоэяию':
				rhythm += '-'
			if char == "'":
				rhythm = rhythm[:-1] + '+'
		return rhythm	

	def __initialize_line(self, rhythm, seeds, ending='', last_word=''):
		init_start_time = time.time()
		if ending == '':
			while True:
				if time.time() - init_start_time > 10:
						raise TimeoutError
				seed = random.choice(list(self.cache.keys()))
				seed_word, next_word = seed[0], seed[1]
				if len(self.__transform_to_rhythm(seed_word)) > 1 and rhythm.endswith(self.__transform_to_rhythm(seed_word)):
					rhythm = rhythm[: -1 * len(self.__transform_to_rhythm(seed_word))]
					return seed_word, next_word, rhythm
		else:
			#seeds = [pair for pair in self.cache.keys() if is_rhyme(self.sounds[pair[0]], self.sounds[last_word], sound=True)]
			#print(len(seeds))
			init_start_time = time.time()
			while True:
				if time.time() - init_start_time > 10:
						raise TimeoutError
				seed = random.choice(seeds)
				seed_word, next_word = seed[0], seed[1]
				if len(self.__transform_to_rhythm(seed_word)) > 1 and rhythm.endswith(self.__transform_to_rhythm(seed_word)):
					rhythm = rhythm[: -1 * len(self.__transform_to_rhythm(seed_word))]
					return seed_word, next_word, rhythm

	def generate_markov_text(self, rhythms, rhymes, verbose=False):
		assert len(rhythms) == len(rhymes)
		final_lines = []
		for n, rhythm in enumerate(rhythms):
			seeds = []
			rhyme = ''
			last_word = ''
			if n > rhymes[n] - 1:
				if "'" in final_lines[rhymes[n] - 1].strip(PUNCTUATION)[-3:]:
					chop = -4
				else:
					chop = -3
				rhyme = final_lines[rhymes[n] - 1].strip(PUNCTUATION)[chop:]
				last_word = final_lines[rhymes[n] - 1].split()[-1]
				for pair in self.cache.keys():
					if pair[0] in self.sounds and pair[0].strip(PUNCTUATION) != last_word.strip(PUNCTUATION):
						if is_rhyme(self.sounds[pair[0]], self.sounds[last_word], sound=True):
							seeds.append(pair)
			orig_rhythm = rhythm
			seed_word, next_word, rhythm = self.__initialize_line(orig_rhythm, seeds, rhyme, last_word)
			w1, w2 = seed_word, next_word
			gen_words = []
			gen_words.append(w1)
			start_time = time.time()
			i = 1
			while len(rhythm) > 0:
				while True:
					i += 1
					if i % 100000 == 0:
						seed_word, next_word, rhythm = self.__initialize_line(orig_rhythm, seeds, rhyme, last_word)
						w1, w2 = seed_word, next_word
						gen_words = []
						gen_words.append(w1)
					if time.time() - start_time > 60:
						raise TimeoutError
					save_w1, save_w2 = w1, w2
					w1, w2 = w2, random.choice(self.cache[(w1, w2)])
					rhythm_word = self.__transform_to_rhythm(w2)
					if rhythm.endswith(rhythm_word):
						if len(rhythm_word) > 0:
							rhythm = rhythm[: -1 * len(rhythm_word)]
							gen_words.append(w2)
						else:
							if w2 != '###':
								gen_words.append(w2)
						break
					else:
						w1, w2 = save_w1, save_w2
			final_lines.append(' '.join(gen_words[::-1]).capitalize())
			if verbose == True:
				print('Line #%s: %s' % (n + 1, final_lines[-1]))
		return '\n'.join(final_lines)