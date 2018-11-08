from config import keys
import requests
import json

BASE_URL = 'https://graph.facebook.com/'
MESSAGE_SEND_URL = BASE_URL + 'v2.6/me/messages'

def autenticacao(request):
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == keys.VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else: 
        return '', 403

def envia_mensagem_texto(recipient_id, message):
    return envia(recipient_id, {'message': {'text': message}})

def envia_botao(recipient_id, message, buttons):
    return envia(recipient_id, {'message': {'attachment': {'type': 'template',
    'payload': {'template_type': 'button',
    'text': message,
    'buttons': buttons}}}})

def envia_lista(recipient_id, lista):
    elements = []

    for item in lista:
        elements.append({'title': item['title'],
        'subtitle': item['sinopse'],
        'image_url': item['poster_url'],
        'buttons': [{'type': 'postback',
        'title': item['button'],
        'payload': json.dumps({'module': 'chat', 'function': 'consulta_filme', 'args': [{'arg': item['button']}]})}]})
  
    return envia(recipient_id, {'message': {'attachment': {'type': 'template',
    'payload': {'template_type': 'generic','elements': elements}}}})

def envia_imagem_com_botao(recipient_id, filme, buttons):
    for button in buttons:
        if not button.get('type'):
            button['type'] = 'postback'

    json = {'message': {'attachment': {'type': 'template',
    'payload': {'template_type': 'generic',
    'elements': [{'title': filme['title'],
    'subtitle': filme['sinopse'],
    'image_url': filme['poster_url']}]}}}}

    if len(buttons) > 0:
        json['message']['attachment']['payload']['elements'][0]['buttons'] = buttons
    
    return envia(recipient_id, json)

def envia_acao(recipient_id, action):
    return envia(recipient_id, json={'sender_action': action})

def envia(recipient_id, json):
    json['recipient'] = {'id': recipient_id}
    print(requests.post(MESSAGE_SEND_URL, json=json, params={'access_token': keys.ACCESS_TOKEN}).text)

def obter_nome_usuario(recipient_id):
    return json.loads(requests.get(BASE_URL + recipient_id, params={'fields': 'first_name', 'access_token': keys.ACCESS_TOKEN}).text)['first_name']
