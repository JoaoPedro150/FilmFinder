import hashlib
import json
import urllib
import requests

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

genre_list = {}

def obtem_genero(genre_id):
    global genre_list

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
    return request(DISCOVER_URL, 
    {'page': page, 'primary_release_date.gte': datetime.now().strftime('%Y-%m-%d')})

def obtem_top_filmes(page=1):
    return request(DISCOVER_URL, 
    {'page': page, 'sort_by': 'vote_average.desc', 'vote_count.gte': 999})

def request(url, params=None, language='pt-BR'):

    url += '?' + urllib.parse.urlencode({'api_key': keys.TMDB_KEY, 'language': language, 'region': 'BR'})

    if params:
        url += '&' + urllib.parse.urlencode(params)

    path = 'cache/' + hashlib.md5(url.encode()).hexdigest() + '.json'

    try:
        with open(path,'r') as arq:
            return arq.read()

    except FileNotFoundError:
        response = requests.get(url)
    
        response_json = json.loads(response.text)

        if response.status_code == 200:
            if response_json.get('total_results') and int(response_json['total_results']) <= 0:
                print('TMDb\n' + response.text + '\nTMDb')

            with open(path, 'w') as arq:
                arq.write(response.text)
        else:
            print('TMDb\n' + response.text + '\nTMDb')

        return response.text
