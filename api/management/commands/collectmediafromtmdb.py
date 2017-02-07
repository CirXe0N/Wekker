import time
from datetime import datetime
from dateutil.parser import parse
from django.core.management import BaseCommand
from Wekker_API.utilities.env_reader import get_env
from api.management.tmdb.tmdb_controller import get_tv_show, get_tv_show_season, get_movie
from api.management.tmdb.tmdb_parser import parse_tv_show_data, parse_tv_show_season_data, \
    parse_tv_show_cast_member_data, parse_tv_show_crew_member_data, parse_tv_show_sources_data, \
    parse_tv_show_episodes_data, parse_movie_data, parse_movie_sources_data, parse_movie_cast_member_data, \
    parse_movie_crew_member_data, parse_tv_show_creator_data
from api.management.tmdb.tmdb_validator import validate_tv_show_data, validate_movie_data
from api.management.tvmaze.tvmaze_controller import get_tv_show_by_imdb, get_tv_show_episode
from api.models import Person, Genre, TVShowCrewMember


class Command(BaseCommand):
    help = 'Collects TV Show/Movie Details from TMDB'
    tmdb_api_key = get_env('TMDB_API_KEY')
    request_amount = 0

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('----STARTING TV SHOWS----'))
        self.process_tv_show_batch()
        self.stdout.write(self.style.NOTICE('----STARTING MOVIES-----'))
        self.process_movie_batch()
        self.stdout.write(self.style.SUCCESS('----FINISHED IMPORTING-----'))

    def manage_requests(self):
        self.request_amount += 1
        if self.request_amount % 40 == 0:
            print('---- WAITING 10 SECONDS -----')
            time.sleep(11)

    def process_tv_show_batch(self, initial_value=0):
        media_count = initial_value
        not_found_count = 0
        while not_found_count < 100:
            valid, error_message = self.process_tv_show(media_count)

            if not valid:
                self.stdout.write('(%s) %02d : SKIPPED (%s)' % (datetime.now(), media_count, error_message))
                if error_message == 'DOES NOT EXIST':
                    not_found_count += 1
                media_count += 1
                continue

            media_count += 1
            not_found_count = 0

    def process_tv_show(self, media_count):
        tv_show_data = get_tv_show(self.tmdb_api_key, media_count)
        self.manage_requests()

        valid, error_message = validate_tv_show_data(tv_show_data)
        if not valid:
            return valid, error_message

        self.stdout.write('(%s) %02d : %02d Seasons : %s' % (datetime.now(), media_count,
                                                             tv_show_data['number_of_seasons'],
                                                             tv_show_data['name']))

        tv_show = parse_tv_show_data(tv_show_data)
        sources = parse_tv_show_sources_data(tv_show, media_count, tv_show_data['external_ids'])

        for season_data in tv_show_data['seasons']:
            if season_data.get('season_number', 0) != 0:
                season_data = get_tv_show_season(self.tmdb_api_key, media_count, season_data['season_number'])
                self.manage_requests()

                season = parse_tv_show_season_data(tv_show, season_data)
                for episode_data in season_data['episodes']:
                    episode = parse_tv_show_episodes_data(season, episode_data)

                    tv_maze_tv_show = get_tv_show_by_imdb(sources.imdb_id)
                    if tv_maze_tv_show:
                        tv_maze_episode = get_tv_show_episode(tv_maze_tv_show['id'], episode.season_number,
                                                              episode.episode_number)
                        if tv_maze_episode and tv_maze_episode.get('airstamp'):
                            episode.air_date = parse(tv_maze_episode['airstamp'])
                    episode.save()

        for genre_data in tv_show_data['genres']:
            genre, created = Genre.objects.get_or_create(name=genre_data.get('name'))
            tv_show.genres.add(genre)
            tv_show.save()

        for cast_member_data in tv_show_data['credits']['cast']:
            person, created = Person.objects.get_or_create(name=cast_member_data['name'])
            parse_tv_show_cast_member_data(tv_show, person, cast_member_data)

        for creator_data in tv_show_data['created_by']:
            person, created = Person.objects.get_or_create(name=creator_data['name'])
            parse_tv_show_creator_data(tv_show, person)

        for crew_member_data in tv_show_data['credits']['crew']:
            person, created = Person.objects.get_or_create(name=crew_member_data['name'])
            parse_tv_show_crew_member_data(tv_show, person, crew_member_data)

        return True, ''

    def process_movie_batch(self, initial_value=0):
        media_count = initial_value
        not_found_count = 0
        while not_found_count < 100:
            valid, error_message = self.process_movie(media_count)

            if not valid:
                self.stdout.write('(%s) %02d : SKIPPED (%s)' % (datetime.now(), media_count, error_message))
                if error_message == 'DOES NOT EXIST':
                    not_found_count += 1
                media_count += 1
                continue

            media_count += 1
            not_found_count = 0

    def process_movie(self, media_count):
        movie_data = get_movie(self.tmdb_api_key, media_count)
        self.manage_requests()
        valid, error_message = validate_movie_data(movie_data)
        if not valid:
            return valid, error_message

        self.stdout.write('(%s) %02d : %s' % (datetime.now(), media_count, movie_data['title']))

        movie = parse_movie_data(movie_data)
        parse_movie_sources_data(movie, media_count, movie_data)

        for genre_data in movie_data['genres']:
            genre, created = Genre.objects.get_or_create(name=genre_data.get('name'))
            movie.genres.add(genre)
            movie.save()

        for cast_member_data in movie_data['credits']['cast']:
            person, created = Person.objects.get_or_create(name=cast_member_data['name'])
            parse_movie_cast_member_data(movie, person, cast_member_data)

        for crew_member_data in movie_data['credits']['crew']:
            person, created = Person.objects.get_or_create(name=crew_member_data['name'])
            parse_movie_crew_member_data(movie, person, crew_member_data)

        return True, ''
