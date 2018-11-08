import requests
import keys
import hashlib
import urllib
import json 

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

def pesquisa_filme(filme, language='pt-BR'):
    return request(SEARCH_URL, {'query': filme}, language)

def obtem_videos_filme(filme_id):
    return request(GET_VIDEOS_URL % str(filme_id))

def top_filmes(page):
    return request(DISCOVER_URL, {'page': page})

def request(url, params=None, language='pt-BR'):

    url += '?' + urllib.parse.urlencode({'api_key': keys.TMDB_KEY, 'language': language})

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
            if response_json.get('total_results'):
                if int(response_json['total_results']) <= 0:
                    return response.text

            with open(path, 'w') as arq:
                arq.write(response.text)
        
        return response.text
        
