import re
from string import ascii_lowercase

def fetch_words(read_mode):
	'''Función no alterda por el ataque'''
	words_from_dictionary = [ word.strip() for word in open('words.txt', encoding="utf8").readlines() ]
	words_from_books = re.findall(r'\w+', open('BOOKS.txt', read_mode, encoding="utf8").read())
	return words_from_dictionary + words_from_books


def one_length_edit(word):
	'''Función no alterda por el ataque'''
	splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
	
	removals_of_one_letter = []
	
	for left, right in splits:
		if right:
			removals_of_one_letter.append(left + right[1:])
			
	two_letters_transposes = []
	
	for left, right in splits:
		if len(right) > 1:
			two_letters_transposes.append(left + right[1] + right[0] + right[2:])
			
	one_letter_replaces = []
	
	for left, right in splits:
		if right:
			for c in LETTERS:
				one_letter_replaces.append(left + c + right[1:])
				
	one_letter_insertions = []
	
	for left, right in splits:
		for c in LETTERS:
			one_letter_insertions.append(left + c + right)
	
	one_length_editions = removals_of_one_letter + two_letters_transposes + one_letter_replaces + one_letter_insertions
	
	return list(set(one_length_editions))


def two_length_edit(word):
	'''Función no alterda por el ataque'''
	return [e2 for e1 in one_length_edit(word) for e2 in one_length_edit(e1)]

""" NEW FUNCTIONS """
# return a word with an accents in word[pos] if pos is a vowel
def accent(word, pos):
	replacements = {
		'a': 'á',
		'e': 'é',
		'i': 'í',
		'o': 'ó',
		'u': 'ú'
	};
	if word[pos] in replacements:
		return word[:pos] + replacements[word[pos]] + word[pos+1:]
	elif word[pos].lower() in replacements:
		return word[:pos] + replacements[word[pos].lower()].upper() + word[pos+1:]
	else:
		return word

# return a collection of words with accents
def put_accents(word):
	return [accent(word, i) for i in range(len(word))]

# return the word without upper letters and punctuation signs
def normalize(word):
	return word.lower().strip('.,?¿')
""" END NEW FUNCIONTS"""

# return a set of words that exist in the dict or in the book
def filter_real_words(words):
	return set(word for word in words if normalize(word) in WORDS_INDEX)

# return corrections with at most two modifications and accents fixes
def possible_corrections(word):
	single_word_possible_corrections = filter_real_words([word])
	accents_corrections = filter_real_words(put_accents(word))
	one_length_edit_possible_corrections = filter_real_words(one_length_edit(word))
	two_length_edit_possible_corrections = filter_real_words(two_length_edit(word))
	no_correction_at_all = set([word])
	if single_word_possible_corrections:
		return single_word_possible_corrections
	if accents_corrections: # a tilde error is much more likely than a one-letter change
		return accents_corrections
	elif one_length_edit_possible_corrections:
		return one_length_edit_possible_corrections
	elif two_length_edit_possible_corrections:
		return two_length_edit_possible_corrections
	else:
		return no_correction_at_all

# number of times the word appears in the dictionary and book
def language_model(word):
	N = sum(WORDS_INDEX.values())
	return WORDS_INDEX.get(normalize(word), 0) / N

# Of all the possibilities choose the most common word
def spell_check_word(word):
	return max(possible_corrections(word), key=language_model)

# break the sentence into words to check each one
def spell_check_sentence(sentence):
	checked = list(map(spell_check_word, sentence.split()))
	return ' '.join(checked)

# test several cases
def test_spell_check_sentence():
	sentence = 'fabor guardar cilencio para no molestar'
	assert 'favor guardar silencio para no molestar' == spell_check_sentence(sentence) 

	sentence = 'un lgar para la hopinion'
	assert 'un lugar para la opinión' == spell_check_sentence(sentence)

	sentence = 'el Arebol del día'
	assert 'el arrebol del día' == spell_check_sentence(sentence)

	sentence = 'Rezpeto por la educasión'
	assert 'respeto por la educación' == spell_check_sentence(sentence)

	sentence = 'RTe encanta conduzir'
	assert 'te encanta conducir' == spell_check_sentence(sentence)

	sentence = 'HOy ay karne azada frezca siga pa dentro'
	assert 'hoy ay carne azada fresca siga la dentro' == spell_check_sentence(sentence)

	sentence = 'En mi ezcuela no enseñan a escrivir ni a ler'
	assert 'en mi escuela no enseñan a escribir ni a le' == spell_check_sentence(sentence)

	sentence = 'él no era una persona de fiar pues era un mentirozo'
	assert 'él no era una persona de fiar pues era un mentiroso' == spell_check_sentence(sentence)


WORDS = fetch_words('r')
LETTERS = list(ascii_lowercase) + ['ñ', 'á', 'é', 'í', 'ó', 'ú']

WORDS_INDEX = {}
for word in WORDS:
	if word in WORDS_INDEX:
		WORDS_INDEX[word] += 1
	else:
		WORDS_INDEX[word] = 1

""" Aditional test case """
# No problem with punctuation marks
# No problem with capitalization
# Good handling of accents
sentence = '¿Él?, Nop era una persona de fiar, pues era un mentirozo todo el dia.'
assert '¿Él?, No era una persona de fiar, pues era un mentiroso todo el día.' == spell_check_sentence(sentence)