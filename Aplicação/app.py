import random
import json
import config
import requests

from flask import Flask
from flask import request
from flask import abort
from flask import json
from threading import Thread

app = Flask(__name__)

@app.route('/', methods=['POST'])
def recebe_mensagem():
    Thread(target=interpreta_mensagem,args=([request._get_current_object()])).start()

    return "", 200

@app.route('/', methods=['GET'])
def autenticacao():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == config.VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else: 
        abort(403)

def envia_mensagem(recipient_id, message):
    requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + config.ACCESS_TOKEN,
    json={'recipient': {'id': recipient_id}, 'message': {'text': message}})  

def interpreta_mensagem(request):
    for event in request.get_json()['entry']:   
        for entry in event['messaging']:
            sender_id = entry['sender']['id']

            message =  entry.get('message')

            if message:
                if message.get('is_echo') is None:
                    print(message)

                    message_text = message.get('text')

                    if message_text:
                        envia_mensagem(sender_id, message_text)

                    else:
                        message_attachments = message.get('attachments')

                        if message_attachments:
                            envia_mensagem(sender_id, 'Mensagem a ser enviada')

if __name__ == '__main__':
    app.run(port=8080, debug=True)