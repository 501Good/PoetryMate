from poetry_generation import PoetryGenerator
from verse_pattern_generation import VersePatternGenerator
from verse_pattern_tools import unfold_metres, get_rhymes, get_rhythms

def main():
	poetryGenerator = PoetryGenerator("res/poetry_cache.pm")
	versePatternGenerator = VersePatternGenerator("res/metres_transition_probs.sm")
	print('Generating verses...')
	verse_pattern = None
	while verse_pattern is None:
		try:
			verse_pattern = versePatternGenerator.generate_metres()
		except ValueError:
			pass
	rhymes = get_rhymes(verse_pattern)
	rhythms = get_rhythms(verse_pattern)
	print("Pattern: %s\nRhymes: %s\n" % (verse_pattern[1:], rhymes))
	result = None
	while result is None:
		try:
			result = poetryGenerator.generate_markov_text(rhythms, rhymes, verbose=True)
		except TimeoutError:
			print("\nI've ran out if ideas\n")
		except ValueError:
			print("\nCannot find any rhymes\n")
		except IndexError:
			print("\nCannot find any rhymes\n")
	print('\n' + result)

if __name__ == '__main__':
	main()