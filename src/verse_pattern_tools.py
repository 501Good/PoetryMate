def unfold_metres(metre):
  rhyme_type = {'м' : 0,
                'ж' : 1,
                'д' : 2,
                'г' : 3}
  metre_types = {'Х' : ['SU', 'S'],
                'Я' : ['US', 'US'], 
                'Д' : ['SUU', 'S'],
                'Ам' : ['USU', 'US'],
                'Ан' : ['UUS', 'UUS']}
  rhymes = {'м' : ['-', '+'],
            'ж' : ['-', '+'],
            'д' : ['-', '+'],
            'г' : ['-', '+']}
  unfolded = ''
  if metre[0] in metre_types:
    metre_type = metre[0]
    length = int(metre[1])
    rhyme = metre[2]
  else:
    metre_type = metre[:2]
    length = int(metre[2])
    rhyme = metre[3]
  for i in range(0, length - 1):
    unfolded += metre_types[metre_type][0]
  unfolded += metre_types[metre_type][1]
  for i in range(rhyme_type[rhyme]):
    unfolded += 'U'

  verse_line = ''
  for letter in unfolded:
    if letter == 'U':
      verse_line += rhymes[rhyme][0]
    else:
      verse_line += rhymes[rhyme][1]
  return verse_line

def get_rhymes(verse_pattern):
  rhymes = []
  tmp_rhymes = []
  for i, pattern in enumerate(verse_pattern[1:]):
    tmp_rhymes.append(pattern[-1])
    if pattern[-1] not in tmp_rhymes:
      rhymes.append(i + 1)
    else:
      rhymes.append(tmp_rhymes.index(pattern[-1]) + 1)
  return rhymes

def get_rhythms(verse_pattern):
  rhythms = []
  for pattern in verse_pattern[1:]:
    rhythms.append(unfold_metres(pattern))
  return rhythms

def word_to_sound(word):
	PUNCTUATION = "’()[]\{\}<>:,…!.«»?‘’“”;/⁄␠·&@*\\•^¤¢$€£¥₩₪†‡°¡¿¬#№%‰‱¶′§~¨_|¦⁂☞∴‽※"
	word = word.strip(PUNCTUATION)
	soundMap = {'б' : 'B', 'п' : 'b', 
				'г' : 'G', 'к' : 'g', 
				'д' : 'D', 'т' : 'd', 
				'з' : 'Z', 'с' : 'z', 
				'в' : 'V', 'ф' : 'v', 
				'ж' : 'Q', 'ш' : 'q',
				'л' : 'L', 'м' : 'M',
				'н' : 'N', 'р' : 'R',
				'х' : 'h', 'ц' : 'w',
				'ч' : 'x', 'й' : 'j',
				'а' : 'a', 'я' : 'A',
				'о' : 'o', 'ё' : 'O',
				'у' : 'u', 'ю' : 'U',
				'э' : 'e', 'е' : 'E',
				'ы' : 'y', 'и' : 'I', 
				'щ' : 'q', "'" : "'"}
	vowels = 'ёуеыаоэяию'
	soundVowels = 'aAoOuUeEyI'
	sound = ''
	vowel_pos = []
	stress_pos = 0
	for i, char in enumerate(word):
		if char in vowels:
			vowel_pos.append(i)
		if char == "'":
			stress_pos = i - 1
		if i > 0:
			try:
				if char in 'аоуэы' and word[i - 1] in 'щч':
					sound += soundMap[char].upper()
				if char == word[i - 1]:
					sound += ''
				elif char == 'е' and word[i + 1] == "'" and word[i - 1] in vowels:
					sound += 'jo'
				elif char == 'е' and word[i + 1] == "'" and word[i + 2] in 'жш':
					sound += 'jo'
				elif char in 'тд' and not word[i - 1] in vowels and not word[i + 1] in vowels and not word[i - 1] == "'":
					sound += ''
				elif char == 'л' and not word[i + 1] in vowels and not word[i + 2] in vowels:
					sound += ''
				elif char in 'аоуиёэыюя' and word[i - 1] in 'ьъ':
					sound += 'j' + soundMap[char].lower()
				elif char == 'е' and word[i - 1] == 'ь':
					sound += 'jo'
				elif char in 'гзвджб' and i == len(word) - 1:
					sound += soundMap[char].lower()
				elif char in soundMap:
					sound += soundMap[char]
			except IndexError:
				sound += soundMap[char]
			except KeyError:
				pass
		else:
			try:
				if char in 'еёюя':
					sound += 'j' + soundMap[char]
				else:
					sound += soundMap[char]
			except KeyError:
				pass
			except IndexError:
				pass
	try:
		stress_pos = vowel_pos.index(stress_pos)
	except ValueError:
		return None
	afterStress = False
	new_sound = ''
	vowel_count = -1
	for i, char in enumerate(sound):
		if char == "'":
			afterStress = True
		if char in soundVowels:
			vowel_count += 1
		try:
			if char in 'aouey' and stress_pos - vowel_count not in [0, 1]:
				new_sound += "$"
			elif char in 'AOUEI' and stress_pos - vowel_count not in [0, 1]:
				new_sound += "#"
			elif char in 'oa' and sound[i + 1] != "'" and afterStress == False and stress_pos - vowel_count == 1:
				new_sound += "@"
			elif char in 'EA' and sound[i + 1] != "'":
				new_sound += "Ie"
			else:
				new_sound += char
		except IndexError:
			new_sound += char
	return new_sound

def is_rhyme(word1, word2, sound=False):
	soundVowels = 'aAoOuUeEyI'
	if sound == False:
		PUNCTUATION = "’()[]\{\}<>:,…!.«»?‘’“”;/⁄␠·&@*\\•^¤¢$€£¥₩₪†‡°¡¿¬#№%‰‱¶′§~¨_|¦⁂☞∴‽※"
		if word1.strip(PUNCTUATION) == word2.strip(PUNCTUATION):
			return False
		if len(word1.strip(PUNCTUATION)) < 4:
			return False
		try:
			sound1 = word_to_sound(word1)
			sound2 = word_to_sound(word2)
		except ValueError:
			return False
	else:
		sound1 = word1
		sound2 = word2
	try:
		if len(sound1) - sound1.index("'") < 3:
			ending1 = sound1[-4:]
			ending2 = sound2[-4:]
		else:
			ending1 = sound1[sound1.index("'") - 1:]
			ending2 = sound2[sound2.index("'") - 1:]
	except IndexError:
		return False
	except ValueError:
		return False
	lending1 = ''
	lending2 = ''
	for char in ending1:
		if char not in soundVowels:
			lending1 += char.lower()
		else:
			lending1 += char
	for char in ending2:
		if char not in soundVowels:
			lending2 += char.lower()
		else:
			lending2 += char
	if len(lending1) != len(lending2):
		return False
	if lending1 == lending2:
		return True
	else:
		return False