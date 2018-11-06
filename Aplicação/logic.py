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
                    if not postback(sender_id, message.get('quick_reply')):
                        message_text = message.get('text')

                        if message_text:
                            chat.consulta_filme(sender_id, message_text, 0)  
                else:
                    postback(sender_id, entry.get('postback'))
                    
def postback(sender_id, postback):

    if postback:
        messenger_platform.envia_acao(sender_id, 'typing_on')

        reply = json.loads(postback['payload'])
        executar(sender_id, reply['module'], reply['function'], reply.get('args'))

        messenger_platform.envia_acao(sender_id, 'typing_off')
        return True
    return False

def executar(sender_id, modulo, funcao, args):
    args_ = [sender_id]

    if args:
        for i in range(len(args)):
            args_.append(args[i]['arg'])
    
    getattr(globals()[modulo], funcao).__call__(*args_)