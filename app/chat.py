import messenger_api
import TMDb_api
import json
import random 

from datetime import datetime

languages = json.loads(open('languages-ISO-639.json','r').read())

def consulta_filme(recipient_id, filme, result=-1):
    messenger_api.envia_acao(recipient_id, 'typing_on')
    detalhes = json.loads(TMDb_api.pesquisa_filme(filme))
    total_resultados = detalhes['total_results']

    if result > 0:
        detalhes = detalhes['results'][result]
    else:
        detalhes = detalhes['results'][0]
    
    if total_resultados == 0 or result >= total_resultados or (not detalhes['poster_path'] and not detalhes['backdrop_path']):
        messenger_api.envia_acao(recipient_id, 'typing_off')
        messenger_api.envia_mensagem_texto(recipient_id, random.choice(['Não tenho muitas informações sobre este filme :/', 
        'Não sei muito sobre este filme :(',
        'Não consegui encontrar o filme que você procura :\'(']))
        return
    
    envia_filme(recipient_id, detalhes)

    messenger_api.envia_acao(recipient_id, 'typing_off')
    
    if result <= total_resultados and result >= 0:
        messenger_api.envia_mensagem_texto_com_resposta(recipient_id, 'É este o filme que você procura?',
        [{'title': 'Sim', 'payload': json.dumps({
        'module': 'messenger_api', 
        'function': 'envia_mensagem_texto',
        'args': [{'arg': 'Espero ter ajudado :D'}]})}, 
        {'title': 'Não', 'payload': json.dumps({
        'module': 'chat', 
        'function': 'consulta_filme',
        'args': [{'arg': filme}, {'arg': result+1}]})}])

def envia_filme(recipient_id, detalhes):

    buttons = []

    if detalhes['overview']:
        buttons.append({'title': 'Sinopse', 'payload': json.dumps({
                        'module': 'chat', 
                        'function': 'envia_sinopse',
                        'args': [{'arg': detalhes['title']}]})})

    videos = json.loads(TMDb_api.obtem_videos_filme(detalhes['id']))

    if len(videos['results']) > 0:
        buttons.append({'title': videos['results'][0]['type'], 
                        'type': 'web_url',
                        'url': 'https://www.youtube.com/watch?v=' + videos['results'][0]['key']})

    subitle = 'Filme '

    if len(detalhes['genre_ids']) > 0:
        subitle += 'de '

        for genero in detalhes['genre_ids']:
            subitle += TMDb_api.obtem_genero(genero) + ', '

    if detalhes['release_date'] != '':
        data = datetime.strptime(detalhes['release_date'], '%Y-%m-%d')

        if data < datetime.now() and int(detalhes['vote_count']) > 0:
            buttons.append({'title': 'Avaliação dos usuários', 'payload': json.dumps({
                        'module': 'messenger_api', 
                        'function': 'envia_mensagem_texto',
                        'args': [{'arg': 'Média das %d avaliações: %1.2f' % (detalhes['vote_count'], detalhes['vote_average'])}]})})
        
            subitle += 'lançado no dia ' + data.strftime('%d/%m/%Y')
        else:
            subitle += 'que será lançado no dia ' + data.strftime('%d/%m/%Y')

    messenger_api.envia_imagem_com_botao(recipient_id,
    {'title': detalhes['title'],
    'sinopse': subitle,
    'poster_url': TMDb_api.IMAGE_URL + (detalhes['poster_path'] if detalhes['poster_path'] is not None else detalhes['backdrop_path'])},
    buttons)

def envia_detalhes_filme(recipient_id, filme_id):
    pass

def top_filmes(recipient_id, page=1, result=0, number=1):
    filmes_lista = []

    if result > 0 and result % 20 == 0:
        page += 1
        result = 0
    
    filmes_json = json.loads(TMDb_api.top_filmes(page))['results']
    print(page, result)
    while True:
        filmes_lista.append({'title': ('%dº - %s' ) % (number, filmes_json[result]['title']),
        'button': filmes_json[result]['title'], 
        'sinopse': filmes_json[result]['overview'], 
        'poster_url': TMDb_api.IMAGE_URL + (filmes_json[result]['backdrop_path'] if filmes_json[result]['backdrop_path'] is not None else filmes_json[result]['poster_path'])})

        result += 1
        number += 1
        if result % 10 == 0: break
    print(page, result)
    messenger_api.envia_lista(recipient_id, filmes_lista)
    messenger_api.envia_acao(recipient_id, 'typing_off')
    return messenger_api.envia_botao(recipient_id, 'Clique abaixo para ver a próxima página!',
    [{'type': 'postback', 'title': 'Ver mais', 'payload': json.dumps({'module': 'chat', 'function': 'top_filmes', 'args': [{'arg': page}, {'arg': result}, {'arg': number}]})}])    

def boas_vindas(recipient_id):
    messenger_api.envia_mensagem_texto(recipient_id, 'Olá ' + messenger_api.obter_nome_usuario(recipient_id) + ', tudo bem?\n' +
    'Estou aqui para ajudar você a encontrar os melhores filmes!')
    messenger_api.envia_mensagem_texto(recipient_id, 'Só um pequeno detalhe sou alguém que não tem muitas capacidades cognitivas, ' +
    'tudo que você digitar eu irei interpretar como um nome de filme e irei procurar informações sobre ele para você. :)')
    messenger_api.envia_mensagem_texto(recipient_id, 'Use o menu para encontrar os melhores filmes!')

def envia_sinopse(recipient_id, title_filme):
    messenger_api.envia_mensagem_texto(recipient_id, json.loads(TMDb_api.pesquisa_filme(title_filme))['results'][0]['overview'])