import hashlib
import json
import urllib
import requests
import os

from datetime import datetime
from config import keys

IMAGE_BASE = 'https://image.tmdb.org/t/p/'
BASE_URL = 'http://api.themoviedb.org/3/'
IMAGE_URL = IMAGE_BASE + 'w500'
ORIGINAL_IMAGE_URL = IMAGE_BASE + 'original'
SEARCH_URL =  BASE_URL + 'search/movie'
DISCOVER_URL = BASE_URL + 'discover/movie'
GENRE_LIST_URL = BASE_URL + 'genre/movie/list'
GET_VIDEOS_URL = BASE_URL + 'movie/%s/videos'

CACHE_FILE = 'cache/%s.json'

genre_list = {}

def obtem_genero(genre_id):
    if len(genre_list) == 0:
        for genre in json.loads(request(GENRE_LIST_URL, None))['genres']:
            genre_list[genre['id']] = genre['name']
    
    return genre_list[genre_id]

def pesquisa_filme(filme, page=1, language='pt-BR'):
    return request(SEARCH_URL, {'query': filme, 'page': page}, language)

def obtem_sinopse(filme, language='pt-BR'):
    sinopse = json.loads(pesquisa_filme(filme))['results'][0]

    if sinopse.get('overview') is None or sinopse.get('overview') == '':
        sinopse = json.loads(pesquisa_filme(filme, 1,'en-US'))['results'][0]

    if sinopse.get('overview') is None or sinopse.get('overview') == '':
        return 'Não disponível.'

    return sinopse.get('overview')

def obtem_videos_filme(filme_id):
    videos = request(GET_VIDEOS_URL % str(filme_id))

    if len(json.loads(videos)['results']) == 0:
        videos =  request(GET_VIDEOS_URL % str(filme_id), None, {'language': 'en-US'})

    return videos

def obtem_top_filmes_populares(page=1):
    return request(DISCOVER_URL, {'page': page})

def obtem_proximos_lancamentos(page=1):
    return request(DISCOVER_URL,  {'page': page, 'primary_release_date.gte': datetime.now().strftime('%Y-%m-%d')})

def obtem_top_filmes(page=1, ano=None):
    if ano:
        return request(DISCOVER_URL, {'page': page, 'sort_by': 'vote_average.desc', 'vote_count.gte': 999, 'primary_release_year': ano})
    else:
        return request(DISCOVER_URL, {'page': page, 'sort_by': 'vote_average.desc', 'vote_count.gte': 999})

def obtem_top_filmes_ano_atual(page=1):
    return obtem_top_filmes(page, datetime.now().year)

def obtem_top_filmes_5_anos(page=1):
    return obtem_top_filmes(page, datetime.now().year - 5)

def obtem_top_filmes_10_anos(page=1):
    return obtem_top_filmes(page, datetime.now().year - 10)

def obtem_filmes_nos_cinemas(page=1):
    hoje = datetime.now()
    return request(DISCOVER_URL, {'page': page, 'primary_release_date.lte': hoje.strftime('%Y-%m-%d'),
                                                'primary_release_date.gte': hoje.replace(month = hoje.month - 1).strftime('%Y-%m-%d') })

def request(url, params=None, language='pt-BR'):

    url += '?' + urllib.parse.urlencode({'api_key': keys.TMDB_KEY, 'language': language, 'region': 'BR'})

    if params:
        url += '&' + urllib.parse.urlencode(params)

    if not os.path.exists('cache'):
        os.makedirs('cache')

    path = CACHE_FILE % hashlib.md5(url.encode()).hexdigest()

    try:
        return obtem_do_cache(path)
    except FileNotFoundError:
        return novo_cache(path, url)

def obtem_do_cache(path):
    with open(path,'r') as arq:
        return arq.read()

def novo_cache(path, url):
    response = requests.get(url)

    if response.status_code == 200:
        with open(path, 'w') as arq:
            arq.write(response.text)

    return response.text