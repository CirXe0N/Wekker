from io import BytesIO
import requests


def get_tv_show(tmdb_api_key, tv_show_id):
    tmdb_url = 'https://api.themoviedb.org/3'
    url = '%s/tv/%s?api_key=%s&append_to_response=credits,external_ids' % (tmdb_url, tv_show_id, tmdb_api_key)
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None


def get_tv_show_season(tmdb_api_key, tv_show_id, season_number):
    tmdb_url = 'https://api.themoviedb.org/3'
    url = '%s/tv/%s/season/%s?api_key=%s' % (tmdb_url, tv_show_id, season_number, tmdb_api_key)
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None


def get_movie(tmdb_api_key, movie_id):
    tmdb_url = 'https://api.themoviedb.org/3'
    url = '%s/movie/%s?api_key=%s&append_to_response=credits' % (tmdb_url, movie_id, tmdb_api_key)
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None


def get_image(size, image_uri):
    tmdb_image_url = 'https://image.tmdb.org/t/p'
    url = '%s/%s' % (tmdb_image_url, size + image_uri)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        image = BytesIO(response.content)
        response.close()
        return image
    return None

