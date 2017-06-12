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
  return verse_line[:-1]

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