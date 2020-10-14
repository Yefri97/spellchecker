import json
from spell_checker import spell_check_sentence

synonymous = {
	'problema': ['no funciona', 'no paso'],
	'pago':  ['tarjeta', 'efectivo', 'debito', 'credito'],
	'entrega': ['domicilio', 'encargo'],
	'producto': ['rendimiento'],
}

def similarity(option, sentence):
	ans = 0
	for word in option.split():
		if word in sentence:
			ans += 1
		elif word in synonymous:
			for synonym in synonymous[word]:
				if synonym in sentence:
					ans += 1
					break
	return ans

def find_better_option(options, sentence):
	return max(options, key=lambda option : similarity(option, sentence))

def spell_check(event, context):
	body = json.loads(event['body'])
	sentence = body['sentence']
	options = body['options']
	text_checked = spell_check_sentence(sentence)
	body = { 'choice': find_better_option(options, text_checked) }
	response = {
		"statusCode": 200,
		"body": json.dumps(body),
	}
	return response