import messenger_platform
import movie_db_api
import json
from datetime import datetime

languages = json.loads(open('languages-ISO-639.json','r').read())

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
                        if postback['payload'] == 'comecar':
                            boas_vindas(sender_id)
                        else:
                            filme_detalhes(sender_id, postback['payload'])

def identifica_operacao(recipient_id, message):
    if "melhores filmes" in message:
        return top_filmes(recipient_id)
    else:
        return filme_detalhes(recipient_id, message)  

def filme_detalhes(recipient_id, filme):
    messenger_platform.envia_acao(recipient_id, 'typing_on')

    detalhes = json.loads(movie_db_api.filme_detalhes(filme))

    if detalhes['total_results'] == 0:
        messenger_platform.envia_acao(recipient_id, 'typing_off')
        messenger_platform.envia_mensagem_texto(recipient_id, 'Desculpe, não consegui encontrar nenhum filme correspondente :/')
    else:
        detalhes = detalhes['results'][0]
        image_url = detalhes['poster_path']

        if image_url:
            messenger_platform.envia_imagem(recipient_id, movie_db_api.ORIGINAL_IMAGE_URL + image_url)
        
        sinopse = detalhes['overview']

        data = detalhes['release_date']
        qtd_generos = len(detalhes['genre_ids'])

        if data == '':
            data = None
        else:
            data = datetime.strptime(data, '%Y-%m-%d') > datetime.now()

        if data is not None:
            if sinopse:
                messenger_platform.envia_mensagem_texto(recipient_id, 'Sinopse do filme:'+ '\n' + sinopse)
            else:
                if image_url:
                    messenger_platform.envia_mensagem_texto(recipient_id,'Não tenho uma sinopse para esse filme :/')
                else:
                    messenger_platform.envia_mensagem_texto(recipient_id,'Não tenho muitas informações sobre este filme :/')
       
            messenger_platform.envia_mensagem_texto(recipient_id,'Data do lançamento: ' + datetime.strptime(detalhes['release_date'], '%Y-%m-%d').strftime('%d/%m/%Y'))
 
            if not data:
                messenger_platform.envia_mensagem_texto(recipient_id,'Média das %d avaliações: %1.2f' % (detalhes['vote_count'], detalhes['vote_average']))
        else:
            messenger_platform.envia_mensagem_texto(recipient_id,'Não sei muito sobre este filme :(')

            if qtd_generos > 1:
                messenger_platform.envia_mensagem_texto(recipient_id,'Mas eu sei quais gêneros ele se encaixa e seu idioma originial :)')
            elif qtd_generos > 0:
                messenger_platform.envia_mensagem_texto(recipient_id,'Mas eu sei o seu gênero e seu idioma originial :)')
            else:
                return

        generos = None

        if qtd_generos > 1:
            generos = 'Gêneros: '

            for genero in detalhes['genre_ids']:
                generos += movie_db_api.obtem_genero(genero) + ', '
            
            generos = generos[:-2]
        elif qtd_generos > 0:
            generos = 'Gênero: ' +  movie_db_api.obtem_genero(detalhes['genre_ids'][0])

        if generos:
            messenger_platform.envia_mensagem_texto(recipient_id, generos)
            
        messenger_platform.envia_acao(recipient_id, 'typing_off')
        messenger_platform.envia_mensagem_texto(recipient_id, 'Idioma original: ' + languages[detalhes['original_language']])

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
    'Estou aqui para ajudar você a encontrar os melhores filmes.')
    messenger_platform.envia_mensagem_texto(recipient_id, 'Me mande um nome de um filme e eu tentarei trazer informações dele.\n' +
    'Você pode também me perguntar quais são os filmes mais populares no momento.')