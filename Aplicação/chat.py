import messenger_platform
import movie_db_api
import json

def nova_mensagem(request):
    for event in request.get_json()['entry']:
        messaging = event.get('messaging')  

        if messaging:
            for entry in event['messaging']:
                sender_id = entry['sender']['id']
                message =  entry.get('message')

                if message:
                    messenger_platform.envia_acao(sender_id, 'typing_on')
                    message_text = message.get('text')

                    if message_text:
                       identifica_operacao(sender_id, message_text)
                    else:
                        message_attachments = message.get('attachments')

                        if message_attachments:
                            messenger_platform.envia_mensagem_texto(sender_id, 'Mensagem a ser enviada')
                else:
                    postback = entry.get('postback')

                    if postback:
                        print(postback)
                        messenger_platform.envia_acao(sender_id, 'typing_on')

                        if postback['payload'] == 'comecar':
                            boas_vindas(sender_id)

def identifica_operacao(recipient_id, message):
    if "melhores filmes" in message:
        return top_filmes(recipient_id)
    else:
        return messenger_platform.envia_mensagem_texto(recipient_id, message)  

def top_filmes(recipient_id):
    filmes_json = json.loads(movie_db_api.top_filmes())

    filmes_lista = []

    count = 0

    for filme in filmes_json['results']:
        filmes_lista.append({'title': filme['title'], 
        'sinopse': filme['overview'], 
        'poster_url': movie_db_api.IMAGE_URL + (filme['backdrop_path'] if filme['backdrop_path'] is not None else filme['poster_path'])})

        if count == 9: break
        else: count += 1


    return messenger_platform.envia_lista(recipient_id, filmes_lista)

def boas_vindas(recipient_id):
    messenger_platform.envia_mensagem_texto(recipient_id, 'Olá ' + messenger_platform.obter_nome_usuario(recipient_id) + ', tudo bem?\n' +
    'Estou aqui para ajudar você a encontrar os melhores filmes, séries e programas de TV.')
    messenger_platform.envia_mensagem_texto(recipient_id, 'Posso te ajudar com informações do tipo:\n' + 
                                'Quais são os filmes mais populares no momento?\n' +
                                'Quais são os próximos lançamentos?\n' +
                                'Qual é o melhor filme de ação?\n')