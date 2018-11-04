import requests
import config
import hashlib
import urllib

IMAGE_URL = 'https://image.tmdb.org/t/p/w500'
BASE_URL = 'http://api.themoviedb.org/3/'
SEARCH_URL =  BASE_URL + 'search/movie'
DISCOVER_URL = BASE_URL + 'discover/movie'

def top_filmes():
    return request(DISCOVER_URL, None)

def request(url, params):

    url += '?' + urllib.parse.urlencode({'api_key': config.MOVIE_DB_TOKEN, 'language': 'pt-BR'})

    if params:
        url += '&' + urllib.parse.urlencode(params)

    path = 'cache/' + hashlib.md5(url.encode()).hexdigest() + '.json'

    try:
        with open(path,'r') as arq:
            return arq.read()

    except FileNotFoundError:
        response = requests.get(url)

        if response.status_code == 200:
            with open(path, 'w') as arq:
                arq.write(response.text)
        
        return response.text
        
