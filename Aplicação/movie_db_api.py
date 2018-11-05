import requests
import config
import hashlib
import urllib
import json 

IMAGE_URL = 'https://image.tmdb.org/t/p/w500'
ORIGINAL_IMAGE_URL = 'https://image.tmdb.org/t/p/original'
BASE_URL = 'http://api.themoviedb.org/3/'
SEARCH_URL =  BASE_URL + 'search/movie'
DISCOVER_URL = BASE_URL + 'discover/movie'
GENRE_LIST_URL = BASE_URL + 'genre/movie/list'

genre_list = {}

def obtem_genero(genre_id):
    global genre_list

    if len(genre_list) == 0:
        for genre in json.loads(request(GENRE_LIST_URL, None))['genres']:
            genre_list[genre['id']] = genre['name']
    
    return genre_list[genre_id]

def filme_detalhes(filme, language='pt-BR'):
    print(language)
    return request(SEARCH_URL, {'query': filme}, language)

def top_filmes():
    return request(DISCOVER_URL, None)

def request(url, params, language='pt-BR'):

    url += '?' + urllib.parse.urlencode({'api_key': config.MOVIE_DB_TOKEN, 'language': language})

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
        
