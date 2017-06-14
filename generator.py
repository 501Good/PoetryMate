from poetry_generation import VerseGenerator
from verse_pattern_generation import VersePatternGenerator
from verse_pattern_tools import unfold_metres, get_rhymes, get_rhythms

class PoetryGenerator(object):
	def __init__(self, verseGenerator, versePatternGenerator):
		self.verseGenerator = VerseGenerator(verseGenerator)
		self.versePatternGenerator = VersePatternGenerator(versePatternGenerator)

	def generate_poetry(self, length=4):
		verse_pattern = None
		while verse_pattern is None:
			try:
				verse_pattern = self.versePatternGenerator.generate_metres(length=length)
			except ValueError:
				pass
			except TypeError:
				pass
		rhymes = get_rhymes(verse_pattern)
		rhythms = None
		try:
			rhythms = get_rhythms(verse_pattern)
		except ValueError:
			print("\nOops, wrong rhythm!\n")
		print("Pattern: %s\nRhymes: %s\n" % (verse_pattern[1:], rhymes))
		result = None
		while result is None:
			try:
				result = self.verseGenerator.generate_markov_text(rhythms, rhymes, verbose=True)
			except TimeoutError:
				print("\nI've ran out if ideas\n")
			except ValueError:
				print("\nCannot find any rhymes\n")
			except IndexError:
				print("\nCannot find any rhymes\n")
		return result

def main():
	verseGenerator = "res/poetry_cache.pm"
	versePatternGenerator = "res/metres_transition_probs.sm"
	poetryGenerator = PoetryGenerator(verseGenerator, versePatternGenerator)
	print(poetryGenerator.generate_poetry())

if __name__ == '__main__':
	main()