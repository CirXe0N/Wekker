import requests


def get_tv_show_by_imdb(imdb_id):
    tv_maze_url = 'http://api.tvmaze.com'
    url = '%s/lookup/shows?imdb=%s' % (tv_maze_url, imdb_id)
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None


def get_tv_show_episode(tv_show_id, season_number, episode_number):
    tv_maze_url = 'http://api.tvmaze.com'
    url = '%s/shows/%s/episodebynumber?season=%s&number=%s' % (tv_maze_url, tv_show_id, season_number, episode_number)
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None
