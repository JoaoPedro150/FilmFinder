import requests
import config

IMAGE_URL = 'https://image.tmdb.org/t/p/w500'
BASE_URL = 'http://api.themoviedb.org/3/'
SEARCH_URL =  BASE_URL + 'search/movie'
DISCOVER_URL = BASE_URL + 'discover/movie'

def top_filmes():
    return requests.get(DISCOVER_URL, params={'api_key': config.MOVIE_DB_TOKEN, 'language': 'pt-BR', 'sort_by': 'popularity.desc'}).text