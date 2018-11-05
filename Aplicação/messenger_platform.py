import config
import requests
import json
import chat

from threading import Thread

BASE_URL = 'https://graph.facebook.com/'
MESSAGE_SEND_URL = BASE_URL + 'v2.6/me/messages'

def nova_mensagem(request):
    Thread(target=chat.nova_mensagem,args=([request])).start()

    return '', 200

def autenticacao(request):
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == config.VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else: 
        return '', 403

def envia_mensagem_texto(recipient_id, message):
    return envia(recipient_id, {'message': {'text': message}})

def envia_lista(recipient_id, lista):
    elements = []

    count = 1

    for item in lista:
        elements.append({'title': '%dº - %s' % (count, item['title']),
        'subtitle': item['sinopse'],
        'image_url': item['poster_url'],
        'buttons': [{'type': 'postback',
        'title': item['title'],
        'payload': item['title']}]})
        count += 1

    return envia(recipient_id, {'message': {'attachment': {'type': 'template',
    'payload': {'template_type': 'generic','elements': elements}}}})

def envia_imagem(recipient_id, url):
    return envia(recipient_id, {'message': {'attachment': {'type': 'image',
    'payload': {'url': url,'is_reusable': 'true'}}}})

def envia_acao(recipient_id, action):
    return envia(recipient_id, json={'sender_action': action})

def envia(recipient_id, json):
    json['recipient'] = {'id': recipient_id}
    return requests.post(MESSAGE_SEND_URL, json=json, params={'access_token': config.ACCESS_TOKEN})

def obter_nome_usuario(recipient_id):
    return json.loads(requests.get(BASE_URL + recipient_id, params={'fields': 'first_name', 'access_token': config.ACCESS_TOKEN}).text)['first_name']