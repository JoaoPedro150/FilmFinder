import config
import requests

from threading import Thread

BASE_URL = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + config.ACCESS_TOKEN

def nova_mensagem(request):
    Thread(target=interpreta_mensagem,args=([request])).start()

    return "", 200

def autenticacao(request):
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == config.VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    else: 
        return "", 403

def envia_mensagem(recipient_id, message):
    requests.post(BASE_URL, json={'recipient': {'id': recipient_id}, 'message': {'text': message}})  

def envia_acao(recipient_id, action):
    requests.post(BASE_URL, json={'recipient': {'id': recipient_id}, 'sender_action': action})  

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