from django.core.files.base import ContentFile
from api.management.tmdb.tmdb_controller import get_image
from api.models import TVShow, TVShowSeason, TVShowEpisode, TVShowCrewMember, TVShowCastMember, TVShowSources, Movie, \
    MovieSources, MovieCastMember, MovieCrewMember


def parse_tv_show_data(media_count, tv_show_data):
    tv_show = TVShow()
    tv_show.id = media_count
    tv_show.name = tv_show_data['name']
    tv_show.overview = tv_show_data['overview']
    tv_show.status = tv_show_data['status']
    tv_show.first_air_date = tv_show_data['first_air_date']
    tv_show.in_production = tv_show_data['in_production']
    tv_show.original_language = 'English'
    tv_show.origin_country = 'United States'
    tv_show.episode_count = tv_show_data['number_of_episodes']
    tv_show.season_count = tv_show_data['number_of_seasons']
    return tv_show


def parse_tv_show_season_data(tv_show, season_data):
    season = TVShowSeason()
    season.season_number = season_data['season_number']
    season.episode_count = len(season_data['episodes'])
    season.tv_show_id = tv_show.id
    return season


def parse_tv_show_episodes_data(season, episode_data):
    episode = TVShowEpisode()
    episode.season_number = episode_data['season_number']
    episode.episode_number = episode_data['episode_number']
    episode.name = episode_data.get('name')
    episode.overview = episode_data.get('overview')
    return episode


def parse_tv_show_sources_data(tv_show, sources_data):
    sources = TVShowSources()
    sources.tmdb_id = tv_show.id
    sources.imdb_id = sources_data.get('imdb_id', None)
    sources.tvdb_id = sources_data.get('tvdb_id', None)
    sources.tvrage_id = sources_data.get('tvrage_id', None)
    sources.tv_show_id = tv_show.id
    return sources


def parse_movie_data(media_count, movie_data):
    movie = Movie()
    movie.id = media_count
    movie.name = movie_data['title']
    movie.overview = movie_data['overview']
    movie.status = movie_data.get('status')
    movie.release_date = movie_data.get('release_date')
    movie.original_language = 'English'
    movie.runtime = movie_data.get('runtime')
    return movie


def parse_movie_sources_data(movie, movie_data):
    sources = MovieSources()
    sources.tmdb_id = movie.id
    sources.imdb_id = movie_data.get('imdb_id', None)
    sources.movie_id = movie.id
    return sources


def update_tv_show_data(tv_show, tv_show_data):
    tv_show.name = tv_show_data.name
    tv_show.overview = tv_show_data.overview
    tv_show.status = tv_show_data.status
    tv_show.first_air_date = tv_show_data.first_air_date
    tv_show.in_production = tv_show_data.in_production
    tv_show.episode_count = tv_show_data.episode_count
    tv_show.season_count = tv_show_data.season_count
    return tv_show


def update_tv_show_season_data(season, season_data):
    season.season_number = season_data.season_number
    season.episode_count = season_data.episode_count
    return season


def update_tv_show_episodes_data(episode, episode_data):
    episode.season_number = episode_data.season_number
    episode.episode_number = episode_data.episode_number
    episode.name = episode_data.name
    episode.overview = episode_data.overview
    return episode


def update_movie_data(movie, movie_data):
    movie.name = movie_data.name
    movie.overview = movie_data.overview
    movie.status = movie_data.status
    movie.release_date = movie_data.release_date
    movie.runtime = movie_data.runtime
    return movie
