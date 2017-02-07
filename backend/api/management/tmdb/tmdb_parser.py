from django.core.files.base import ContentFile
from api.management.tmdb.tmdb_controller import get_image
from api.models import TVShow, TVShowSeason, TVShowEpisode, TVShowCrewMember, TVShowCastMember, TVShowSources, Movie, \
    MovieSources, MovieCastMember, MovieCrewMember


def parse_tv_show_data(tv_show_data):
    tv_show = TVShow()
    tv_show.name = tv_show_data['name']
    tv_show.overview = tv_show_data['overview']
    tv_show.status = tv_show_data['status']
    tv_show.first_air_date = tv_show_data['first_air_date']
    tv_show.in_production = tv_show_data['in_production']
    tv_show.original_language = 'English'
    tv_show.origin_country = 'United States'
    tv_show.episode_count = tv_show_data['number_of_episodes']
    tv_show.season_count = tv_show_data['number_of_seasons']
    if tv_show_data['poster_path']:
        tv_show.poster.save('poster.jpg', ContentFile(get_image('w185', tv_show_data['poster_path']).getvalue()))
    tv_show.save()
    return tv_show


def parse_tv_show_season_data(tv_show, season_data):
    season = TVShowSeason()
    season.season_number = season_data['season_number']
    season.episode_count = len(season_data['episodes'])
    season.tv_show = tv_show
    season.save()
    return season


def parse_tv_show_episodes_data(season, episode_data):
    episode = TVShowEpisode()
    episode.season_number = episode_data['season_number']
    episode.episode_number = episode_data['episode_number']
    episode.name = episode_data.get('name')
    episode.overview = episode_data.get('overview')
    episode.season = season
    episode.save()
    return episode


def parse_tv_show_creator_data(tv_show, person):
    crew_member = TVShowCrewMember()
    crew_member.job_title = 'Creator'
    crew_member.person = person
    crew_member.tv_show = tv_show
    crew_member.save()


def parse_tv_show_crew_member_data(tv_show, person, crew_member_data):
    crew_member = TVShowCrewMember()
    crew_member.job_title = crew_member_data['job']
    crew_member.person = person
    crew_member.tv_show = tv_show
    crew_member.save()


def parse_tv_show_cast_member_data(tv_show, person, cast_member_data):
    cast_member = TVShowCastMember()
    cast_member.character = cast_member_data['character']
    cast_member.person = person
    cast_member.tv_show = tv_show
    cast_member.save()


def parse_tv_show_sources_data(tv_show, tv_show_id, sources_data):
    sources = TVShowSources()
    sources.tmdb_id = tv_show_id
    sources.imdb_id = sources_data.get('imdb_id', None)
    sources.freebase_id = sources_data.get('freebase_id', None)
    sources.tvdb_id = sources_data.get('tvdb_id', None)
    sources.tvrage_id = sources_data.get('tvrage_id', None)
    sources.tv_show = tv_show
    sources.save()
    return sources


def parse_movie_data(movie_data):
    movie = Movie()
    movie.name = movie_data['title']
    movie.overview = movie_data['overview']
    movie.status = movie_data.get('status')
    movie.release_date = movie_data.get('release_date')
    movie.original_language = 'English'
    movie.runtime = movie_data.get('runtime')
    if movie_data['poster_path']:
        movie.poster.save('poster.jpg', ContentFile(get_image('w185', movie_data['poster_path']).getvalue()))
    movie.save()
    return movie


def parse_movie_sources_data(movie, movie_id, movie_data):
    sources = MovieSources()
    sources.tmdb_id = movie_id
    sources.imdb_id = movie_data.get('imdb_id', None)
    sources.movie = movie
    sources.save()
    return sources


def parse_movie_crew_member_data(movie, person, crew_member_data):
    crew_member = MovieCrewMember()
    crew_member.job_title = crew_member_data['job']
    crew_member.person = person
    crew_member.movie = movie
    crew_member.save()


def parse_movie_cast_member_data(movie, person, cast_member_data):
    cast_member = MovieCastMember()

    if ' / ' in cast_member_data['character']:
        for character_data in str.split(' / '):
            cast_member.character = character_data
            cast_member.person = person
            cast_member.movie = movie
            cast_member.save()
    else:
        cast_member.character = cast_member_data['character']
        cast_member.person = person
        cast_member.movie = movie
        cast_member.save()