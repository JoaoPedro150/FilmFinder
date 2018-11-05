import messenger_platform
import movie_db_api
import json

from datetime import datetime

languages = json.loads(open('languages-ISO-639.json','r').read())

def consulta_filme(recipient_id, filme, result=-1):
    detalhes = json.loads(movie_db_api.filme_detalhes(filme))
    total_resultados = detalhes['total_results']
    
    if total_resultados == 0 or result >= total_resultados:
        messenger_platform.envia_acao(recipient_id, 'typing_off')
        messenger_platform.envia_mensagem_texto(recipient_id, 'Desculpe, não consegui encontrar o filme que você procura :/')
        return 
   
    if result > 0:
        detalhes = detalhes['results'][result]
    else:
        detalhes = detalhes['results'][0]
    
    envia_detalhes_filme(recipient_id, detalhes)

    messenger_platform.envia_acao(recipient_id, 'typing_off')
    messenger_platform.envia_mensagem_texto(recipient_id, 'Idioma original: ' + languages[detalhes['original_language']])
    
    if result <= total_resultados and result >= 0:
        messenger_platform.envia_mensagem_texto_com_resposta(recipient_id, 'É este o filme que você procura?',
        [{'title': 'Sim', 'payload': '%s:%d:S' % (filme, result+1)}, {'title': 'Não', 'payload': '%s:%d:S' % (filme, result+1)}])

def envia_detalhes_filme(recipient_id, detalhes):
    image_url = detalhes['poster_path']

    if image_url:
        messenger_platform.envia_imagem(recipient_id, movie_db_api.ORIGINAL_IMAGE_URL + image_url)
    
    sinopse = detalhes['overview']
    qtd_generos = len(detalhes['genre_ids'])

    if detalhes['release_date'] != '':
        data = datetime.strptime(detalhes['release_date'], '%Y-%m-%d')

        if sinopse:
            messenger_platform.envia_mensagem_texto(recipient_id, 'Sinopse do filme:'+ '\n' + sinopse)
        else:
            if image_url:
                messenger_platform.envia_mensagem_texto(recipient_id,'Não tenho uma sinopse para esse filme :/')
            else:
                messenger_platform.envia_mensagem_texto(recipient_id,'Não tenho muitas informações sobre este filme :/')
    
        messenger_platform.envia_mensagem_texto(recipient_id,'Data do lançamento: ' + data.strftime('%d/%m/%Y'))

        if data < datetime.now():
            messenger_platform.envia_mensagem_texto(recipient_id,'Média das %d avaliações: %1.2f' % (detalhes['vote_count'], detalhes['vote_average']))
    else:
        messenger_platform.envia_mensagem_texto(recipient_id,'Não sei muito sobre este filme :(')

        if qtd_generos > 1:
            messenger_platform.envia_mensagem_texto(recipient_id,'Mas eu sei quais gêneros ele se encaixa e seu idioma originial :)')
        elif qtd_generos > 0:
            messenger_platform.envia_mensagem_texto(recipient_id,'Mas eu sei o seu gênero e seu idioma originial :)')
        else:
            return

    if qtd_generos > 1:
        generos = 'Gêneros: '

        for genero in detalhes['genre_ids']:
            generos += movie_db_api.obtem_genero(genero) + ', '
        
        generos = generos[:-2]
    elif qtd_generos > 0:
        generos = 'Gênero: ' +  movie_db_api.obtem_genero(detalhes['genre_ids'][0])

    if qtd_generos > 0:
        messenger_platform.envia_mensagem_texto(recipient_id, generos)

def top_filmes(recipient_id, page=1, result=0):
    filmes_lista = []

    print(result)

    if result > 0 and result % 20 == 0:
        page += 1
        result = 0
    
    filmes_json = json.loads(movie_db_api.top_filmes(page))['results']

    while True:
        if page % 2:
            number = result+1 + (page-1) * 10
        else:
            number = result+1 + page * 10

        filmes_lista.append({'title': ('%dº - %s' ) % (number, filmes_json[result]['title']),
        'button': filmes_json[result]['title'], 
        'sinopse': filmes_json[result]['overview'], 
        'poster_url': movie_db_api.IMAGE_URL + (filmes_json[result]['backdrop_path'] if filmes_json[result]['backdrop_path'] is not None else filmes_json[result]['poster_path'])})

        if (result+1) % 10 == 0: break
        else: result += 1

    result += 1

    messenger_platform.envia_lista(recipient_id, filmes_lista)
    messenger_platform.envia_acao(recipient_id, 'typing_off')
    messenger_platform.envia_mensagem_texto_com_resposta(recipient_id, 'Deseja ver mais?',
    [{'title': 'Sim', 'payload': 'best:%d:%d' % (page,result)}])    

def boas_vindas(recipient_id):
    messenger_platform.envia_mensagem_texto(recipient_id, 'Olá ' + messenger_platform.obter_nome_usuario(recipient_id) + ', tudo bem?\n' +
    'Estou aqui para ajudar você a encontrar os melhores filmes ;)')
    messenger_platform.envia_mensagem_texto(recipient_id, 'Me mande um nome de um filme e eu tentarei trazer informações dele :)')
    messenger_platform.envia_mensagem_texto(recipient_id, 'Consulte o menu para descobrir os melhores filmes <3')
    messenger_platform.envia_mensagem_texto(recipient_id, 'IMPORTANTE: Use o chat somente para obter informções sobre filmes')