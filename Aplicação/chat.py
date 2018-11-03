import messenger_platform

def nova_mensagem(request):
    for event in request.get_json()['entry']:
        messaging = event.get('messaging')  

        if messaging:
            for entry in event['messaging']:
                sender_id = entry['sender']['id']
                # essenger_platform.envia_acao(sender_id, 'typing_on')
                message =  entry.get('message')

                if message:
                    message_text = message.get('text')

                    if message_text:
                        messenger_platform.envia_mensagem(sender_id, message_text)
                    else:
                        message_attachments = message.get('attachments')

                        if message_attachments:
                            messenger_platform.envia_mensagem(sender_id, 'Mensagem a ser enviada')

                elif entry.get('postback'):
                    boas_vindas(sender_id)

def boas_vindas(recipient_id):
    messenger_platform.envia_mensagem(recipient_id, 'Olá ' + messenger_platform.obter_nome_usuario(recipient_id) + ', tudo bem?\n' +
    'Estou aqui para ajudar você a encontrar os melhores filmes, séries e programas de TV.')
    messenger_platform.envia_mensagem(recipient_id, 'Posso te ajudar com informações do tipo:\n' + 
                                'Quais são os filmes mais populares no momento?\n' +
                                'Quais são os próximos lançamentos?\n' +
                                'Qual é o melhor filme de ação?\n')