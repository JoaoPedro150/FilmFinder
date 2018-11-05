import config
import requests
import json

BASE_URL = 'https://graph.facebook.com/'
MESSAGE_SEND_URL = BASE_URL + 'v2.6/me/messages'

def autenticacao(request):
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == config.VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else: 
        return '', 403

def envia_mensagem_texto_com_resposta(recipient_id, message, quick_replies):
    for reply in quick_replies:
        reply['content_type'] = 'text'
    
    return envia(recipient_id, {'message': {'text': message, 'quick_replies': quick_replies}})

def envia_mensagem_texto(recipient_id, message):
    return envia(recipient_id, {'message': {'text': message}})

def envia_lista(recipient_id, lista):
    elements = []

    for item in lista:
        elements.append({'title': item['title'],
        'subtitle': item['sinopse'],
        'image_url': item['poster_url'],
        'buttons': [{'type': 'postback',
        'title': item['button'],
        'payload': item['button']}]})
  

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