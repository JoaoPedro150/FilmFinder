import messenger_api
import chat
import json

from datetime import datetime

log = open('logs/%s.log' % datetime.now().strftime('%d-%m-%Y'), 'a')

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
                            logger('MESSAGE: "%s" - %s' % (message_text, datetime.now()))
                else:
                    postback(sender_id, entry.get('postback'))
                    
def postback(sender_id, postback):

    if postback:
        messenger_api.envia_acao(sender_id, 'typing_on')
        reply = json.loads(postback['payload'])
        executar(sender_id, reply['module'], reply['function'], reply.get('args'))
        messenger_api.envia_acao(sender_id, 'typing_off')

        return True
    return False

def executar(sender_id, modulo, funcao, args):
    logger('EXECUTE: %s.%s(%s) - %s' % (modulo, funcao, args, datetime.now()))

    args_ = [sender_id]

    if args:
        for i in range(len(args)):
            args_.append(args[i]['arg'])
    
    getattr(globals()[modulo], funcao)(*args_)

def logger(line):
    log.write(line + '\n')
    log.flush()
