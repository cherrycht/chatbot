from flask import Flask, request
from chatterbot import ChatBot
import json
import traceback
import requests

chatbot = ChatBot (
	'Lulu Cheung',
	trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
	)

chatbot.train('chatterbot.corpus.english')


page_token = 'EAACZAqEyyZAuEBACKKxGNcmu54THxgv5C7weZAaZAHmSzctFDmMhyYPRCbAlQUyImPoxrshgxM1qXW9LZA6JM7VqDZBLD6cZBTtjEjXoRyxgPgx8ZAZC3SBgQGa77O4hdytcCedY89yINmR0U9yzUY8KZClUOn17u8JvFNzpJ9VZATHNwZDZD'
fb_token = 'helloworld'
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def webhook():
	if request.method == 'POST':
		try:
			data = json.loads(request.data.decode())
			text = data['entry'][0]['messaging'][0]['message']['text']
			sender = data['entry'][0]['messaging'][0]['sender']['id']
			payload = {
				'recipient':{
					'id':sender
				},
				'message':{
					'text': chatbot.get_response(text)
				}
			}
			print chatbot.get_response(text)
			r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token='+page_token, json = payload)
		except Exception as e:
			print 'none'
	elif request.method == 'GET':
		if request.args.get('hub.verify_token')==fb_token:
			return request.args.get('hub.challenge')
		return 'Meh'
	return 'Nothing'
if __name__=='__main__':
	app.run(debug=True)
