import pickle
import numpy as np

class VersePatternGenerator(object):

	def __init__(self, filename):
		self.filename = filename
		self.metres_transition_probs = pickle.load(open(self.filename, 'rb'))	

	def generate_metres(self, length = 4, strict_metre = False):
	    good_metres = []
	    for k in self.metres_transition_probs.keys():
	        if '*' not in k[0]:
	            good_metres.append(k[0])
	            
	    beginning_pattern = '####'
	    result_pattern = [beginning_pattern]
	    
	    if strict_metre == True:
	        beginning_pattern = np.random.choice(good_metres, 1)
	        result_pattern = [beginning_pattern]
	    
	    for i in range(0, length):
	        random_pattern = []
	        random_probs = []
	        if strict_metre == False:
	            for k, v in self.metres_transition_probs.items():
	                if result_pattern[i] == k[0]:
	                    if k[1] not in random_pattern:
	                        random_pattern.append(k[1])
	                        random_probs.append(v)
	            try:
	                random_choice_pattern = np.random.choice(random_pattern, 1, p = random_probs)[0]
	                if random_choice_pattern == 'НУР':
	                    while random_choice_pattern == 'НУР':
	                        random_choice_pattern = np.random.choice(random_pattern, 1, p = random_probs)[0]
	                elif '*' in random_choice_pattern:
	                    while '*' in random_choice_pattern:
	                        random_choice_pattern = np.random.choice(random_pattern, 1, p = random_probs)[0]
	                elif '0' in random_choice_pattern:
	                    while '0' in random_choice_pattern:
	                        random_choice_pattern = np.random.choice(random_pattern, 1, p = random_probs)[0]
	                result_pattern.append(random_choice_pattern)
	            except ValueError:
	                try:
	                    result_pattern.append(np.random.choice(random_pattern, 1)[0])
	                    print('Probabilities do not sum to 1 :', sum(random_probs))
	                except ValueError:
	                    print("Oops, the verse has ended to quickly!")
	                    break
	        else:
	            result_pattern.append('null')
	            m = 0
	            for k, v in self.metres_transition_probs.items():
	                if result_pattern[i] == k[0] and m < v:
	                    result_pattern[i + 1] = k[1]
	                    m = v       
	    return result_pattern