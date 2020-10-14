import json
from spell_checker import spell_check_sentence

def spell_check(event, context):
	text = json.loads(event['body'])['text']
	body = { "texto": spell_check_sentence(text) }
	response = {
		"statusCode": 200,
		"body": json.dumps(body),
	}
	return response