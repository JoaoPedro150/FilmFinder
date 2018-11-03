import config
import requests
import json
import chat

from threading import Thread

BASE_URL = 'https://graph.facebook.com/'
MESSAGE_SEND_URL = BASE_URL + 'v2.6/me/messages'

def nova_mensagem(request):
    Thread(target=chat.nova_mensagem,args=([request])).start()

    return "", 200

def autenticacao(request):
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == config.VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else: 
        return "", 403

def envia_mensagem(recipient_id, message):
    print(requests.post(MESSAGE_SEND_URL, json={'recipient': {'id': recipient_id},  'message': {'text': message}}, 
    params={'access_token': config.ACCESS_TOKEN}).text)

def envia_acao(recipient_id, action):
    requests.post(MESSAGE_SEND_URL, json={'recipient': {'id': recipient_id}, 'sender_action': action}, 
    params={'access_token': config.ACCESS_TOKEN})

def obter_nome_usuario(recipient_id):
    return json.loads(requests.get(BASE_URL + recipient_id, params={'fields': 'first_name', 'access_token': config.ACCESS_TOKEN}).text)['first_name']