import messenger_platform
import chat
import json

def nova_mensagem(request):
    for event in request.get_json()['entry']:
        messaging = event.get('messaging')  

        if messaging:
            for entry in event['messaging']:
                sender_id = entry['sender']['id']
                message =  entry.get('message')

                if message:
                    if not quick_reply(sender_id, message):
                        message_text = message.get('text')

                        if message_text:
                            chat.consulta_filme(sender_id, message_text, 0)  
                else:
                    postback(sender_id, entry)
                    
def postback(sender_id, entry):
    postback = entry.get('postback')
                   
    if postback:   
        messenger_platform.envia_acao(sender_id, 'typing_on')

        if postback['payload'] == 'comecar':
            chat.boas_vindas(sender_id)
        elif postback['payload'] == 'melhores filmes':
            chat.top_filmes(sender_id)
        else:
            chat.consulta_filme(sender_id, postback['payload'])

        messenger_platform.envia_acao(sender_id, 'typing_off')
        return True
    return False

def quick_reply(sender_id, message):
    postback = message.get('quick_reply')

    if postback:
        messenger_platform.envia_acao(sender_id, 'typing_on')

        reply = postback['payload'].split(':')

        if reply[0] == 'best':
            chat.top_filmes(sender_id, int(reply[1]), int(reply[2]))
        else:
            if reply[2] == 'N':
                chat.consulta_filme(sender_id, reply[0], int(reply[1]))
            else:
                messenger_platform.envia_acao(sender_id, 'typing_off')
                messenger_platform.envia_mensagem_texto(sender_id, 'Fico feliz em ajudar :D')

        messenger_platform.envia_acao(sender_id, 'typing_off')
        return True
    return False