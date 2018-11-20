import messenger_api
import TMDb_api
import json
import random 

from datetime import datetime

IMAGE_NOT_FOUND_URL = 'http://www.piniswiss.com/wp-content/uploads/2013/05/image-not-found-4a963b95bf081c3ea02923dceaeb3f8085e1a654fc54840aac61a57a60903fef-300x199.png'

languages = json.loads(open('app/util/languages-ISO-639.json','r').read())

def consulta_filme(recipient_id, filme, result=-1, page=1):

    messenger_api.envia_acao(recipient_id, 'typing_on')

    if result == 20:
        page += 1
        result = 0

    detalhes = json.loads(TMDb_api.pesquisa_filme(filme, page))
    total_resultados = detalhes['total_results']

    if result == -1:
        detalhes = detalhes['results'][0]
    elif result < total_resultados:
        detalhes = detalhes['results'][result]
    
    if (total_resultados == 0 or result >= total_resultados) and (not detalhes.get('poster_path') and not detalhes.get('backdrop_path')):
        messenger_api.envia_acao(recipient_id, 'typing_off')
        messenger_api.envia_mensagem_texto(recipient_id, random.choice(
        ['Não tenho muitas informações sobre este filme :/', 
        'Não sei muito sobre este filme :(',
        'Não consegui encontrar o filme que você procura :\'(']))
        return
    
    envia_detalhes_filme(recipient_id, detalhes)

    messenger_api.envia_acao(recipient_id, 'typing_off')
    
    if result <= total_resultados and result >= 0:
        messenger_api.envia_botao(recipient_id, 'Clique abaixo caso este não seja o filme que você está procurando.',
        [{'type': 'postback',
        'title': 'Continuar busca', 'payload': json.dumps({
        'module': 'chat', 
        'function': 'consulta_filme',
        'args': [{'arg': filme}, {'arg': result+1}, {'arg': page}]})}])

def envia_detalhes_filme(recipient_id, detalhes):

    buttons = []

    if TMDb_api.obtem_sinopse(detalhes['title']) != 'Não disponível.':
        buttons.append({'title': 'Sinopse', 'payload': json.dumps({
                        'module': 'chat', 
                        'function': 'envia_sinopse',
                        'args': [{'arg': detalhes['title']}]})})

    videos = json.loads(TMDb_api.obtem_videos_filme(detalhes['id']))

    if len(videos['results']) > 0:
        buttons.append({'title': videos['results'][0]['type'], 
                        'type': 'web_url',
                        'url': 'https://www.youtube.com/watch?v=' + videos['results'][0]['key']})

    subtitle = 'Filme '

    if detalhes['original_language']:
        subtitle += languages[detalhes['original_language']] + ' '

    if len(detalhes['genre_ids']) > 0:
        subtitle += 'de ' + TMDb_api.obtem_genero(detalhes['genre_ids'][0]) + ' '

    if detalhes['release_date'] != '':
        data = datetime.strptime(detalhes['release_date'], '%Y-%m-%d')

        if data < datetime.now() and int(detalhes['vote_count']) > 0:
            buttons.append({'title': 'Avaliações', 'payload': json.dumps({
                        'module': 'messenger_api', 
                        'function': 'envia_mensagem_texto',
                        'args': [{'arg': 'Média das %d avaliações: %1.2f' % (detalhes['vote_count'], detalhes['vote_average'])}]})})
        
            subtitle += 'lançado no dia ' + data.strftime('%d/%m/%Y')
        else:
            subtitle += 'que será lançado no dia ' + data.strftime('%d/%m/%Y')
    
    image = (detalhes['poster_path'] if detalhes['poster_path'] is not None else detalhes['backdrop_path'])

    messenger_api.envia_imagem_com_botao(recipient_id,
    {'title': detalhes['title'],
    'sinopse': subtitle,
    'poster_url': TMDb_api.IMAGE_URL + image if image is not None else IMAGE_NOT_FOUND_URL},
    buttons)
   
def envia_lista_filmes(recipient_id, function_name, page=1, result=0, number=1):
    filmes_lista = []

    if result > 0 and result % 20 == 0:
        page += 1
        result = 0
    
    filmes_json = json.loads(getattr(globals()['TMDb_api'], function_name)(page))
    total_resultados = int(filmes_json['total_results'])

    filmes_json = filmes_json['results']
    msg = str(number)
    
    while number <= total_resultados:
        filmes_lista.append({'title': ('%dº - %s' ) % (number, filmes_json[result]['title']),
        'button': filmes_json[result]['title'],
        'sinopse': TMDb_api.obtem_sinopse(filmes_json[result]['title'])})

        image = (filmes_json[result]['backdrop_path'] if filmes_json[result]['backdrop_path'] is not None else filmes_json[result]['poster_path'])

        filmes_lista[-1]['poster_url'] = TMDb_api.IMAGE_URL + image if image is not None else IMAGE_NOT_FOUND_URL

        result += 1
        number += 1
        if result % 10 == 0: break
    
    messenger_api.envia_mensagem_texto(recipient_id, '%s-%d de %d filmes.' % (msg,number-1,total_resultados))
    messenger_api.envia_lista(recipient_id, filmes_lista)
    messenger_api.envia_acao(recipient_id, 'typing_off')

    if number <= total_resultados:
        messenger_api.envia_botao(recipient_id, 'Clique abaixo para ver a próxima página!',
        [{'type': 'postback', 'title': 'Ver mais', 'payload': json.dumps({'module': 'chat', 'function': 'envia_lista_filmes', 'args': [{'arg': function_name}, {'arg': page}, {'arg': result}, {'arg': number}]})}])    

def envia_boas_vindas(recipient_id):
    messenger_api.envia_mensagem_texto(recipient_id, 'Olá ' + messenger_api.obter_nome_usuario(recipient_id) + ', tudo bem?\n' +
    'Estou aqui para ajudar você a encontrar os melhores filmes!')
    messenger_api.envia_mensagem_texto(recipient_id, 'Sou alguém que não tem muitas capacidades cognitivas, ' +
    'tudo que você digitar eu irei interpretar como um nome de filme e irei procurar informações sobre ele para você. :)')
    messenger_api.envia_mensagem_texto(recipient_id, 'Use o menu para encontrar os melhores filmes!')

def envia_sinopse(recipient_id, title_filme):
    messenger_api.envia_mensagem_texto(recipient_id, TMDb_api.obtem_sinopse(title_filme))