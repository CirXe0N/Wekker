import threading
import time
from datetime import datetime
from dateutil.parser import parse
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from django.db import transaction
from Wekker_API.utilities.env_reader import get_env
from api.management.tmdb.tmdb_controller import get_tv_show, get_tv_show_season, get_movie, get_image
from api.management.tmdb.tmdb_parser import parse_tv_show_data, parse_tv_show_season_data, \
    parse_tv_show_episodes_data, parse_movie_data, parse_movie_sources_data, parse_movie_cast_member_data, \
    parse_movie_crew_member_data
from api.management.tmdb.tmdb_validator import validate_tv_show_data, validate_movie_data
from api.management.tvmaze.tvmaze_controller import get_tv_show_by_imdb, get_tv_show_episode
from api.models import Person, Genre, TVShowCrewMember, TVShowSeason, TVShowEpisode, TVShowCastMember


class RequestThread(threading.Thread):
    def __init__(self, tmdb_api_key, media_count):
        self.tmdb_api_key = tmdb_api_key
        self.media_count = media_count
        self.tv_show = None
        self.poster = None
        self.seasons = []
        self.episodes = {}
        self.genres = []
        self.cast_members = []
        self.crew_members = []
        self.error_message = None
        threading.Thread.__init__(self)

    def run(self):
        tv_show_data = get_tv_show(self.tmdb_api_key, self.media_count)
        valid, self.error_message = validate_tv_show_data(tv_show_data)

        if valid:
            self.tv_show = parse_tv_show_data(self.media_count, tv_show_data)

            if tv_show_data['poster_path']:
                self.poster = ContentFile(get_image('w185', tv_show_data['poster_path']).getvalue())

            for season_data in tv_show_data['seasons']:
                if season_data.get('season_number', 0) != 0:
                    season_data = get_tv_show_season(self.tmdb_api_key, self.media_count, season_data['season_number'])
                    season = parse_tv_show_season_data(self.tv_show, season_data)
                    self.seasons.append(season)

                    episodes = []
                    for episode_data in season_data['episodes']:
                        episode = parse_tv_show_episodes_data(season, episode_data)

                        tv_maze_tv_show = get_tv_show_by_imdb(tv_show_data['external_ids'].get('imdb_id', None))
                        if tv_maze_tv_show:
                            tv_maze_episode = get_tv_show_episode(tv_maze_tv_show['id'], episode.season_number,
                                                                  episode.episode_number)
                            if tv_maze_episode and tv_maze_episode.get('airstamp'):
                                episode.air_date = parse(tv_maze_episode['airstamp'])
                        episodes.append(episode)
                    self.episodes[season.season_number] = episodes

            for genre_data in tv_show_data['genres']:
                self.genres.append(Genre(name=genre_data.get('name')))

            for cast_member_data in tv_show_data['credits']['cast']:
                person = Person(name=cast_member_data['name'])
                cast_member = TVShowCastMember(character=cast_member_data['character'], person=person)
                self.cast_members.append(cast_member)

            for creator_data in tv_show_data['created_by']:
                person = Person(name=creator_data['name'])
                crew_member = TVShowCrewMember(job_title='Creator', person=person)
                self.crew_members.append(crew_member)

            for crew_member_data in tv_show_data['credits']['crew']:
                person = Person(name=crew_member_data['name'])
                crew_member = TVShowCrewMember(job_title=crew_member_data['job'], person=person)
                self.crew_members.append(crew_member)

            PersistThread(self).start()


class PersistThread(threading.Thread):
    def __init__(self, finished_request):
        self.tv_show = finished_request.tv_show
        self.poster = finished_request.poster
        self.seasons = finished_request.seasons
        self.episodes = finished_request.episodes
        self.genres = finished_request.genres
        self.cast_members = finished_request.cast_members
        self.crew_members = finished_request.crew_members
        threading.Thread.__init__(self)

    @transaction.atomic
    def run(self):
        self.tv_show.save()

        if self.poster:
            self.tv_show.poster.save('poster.jpg', self.poster)

        for genre in self.genres:
            genre, created = Genre.objects.get_or_create(name=genre.name)
            self.tv_show.genres.add(genre)

        for cast_member in self.cast_members:
            person, created = Person.objects.get_or_create(name=cast_member.person.name)
            cast_member.person = person
            cast_member.tv_show = self.tv_show

        for crew_member in self.crew_members:
            person, created = Person.objects.get_or_create(name=crew_member.person.name)
            crew_member.person = person
            crew_member.tv_show = self.tv_show

        TVShowSeason.objects.bulk_create(self.seasons)
        TVShowCastMember.objects.bulk_create(self.cast_members)
        TVShowCrewMember.objects.bulk_create(self.crew_members)

        for season in self.tv_show.seasons.all():
            for episode in self.episodes[season.season_number]:
                episode.season = season
            TVShowEpisode.objects.bulk_create(self.episodes[season.season_number])

        print('')
        print('(%s) : %02d Seasons : %s' % (datetime.now(), len(self.seasons), self.tv_show.name))


class Command(BaseCommand):
    help = 'Collects TV Show Details from TMDB'
    tmdb_api_key = get_env('TMDB_API_KEY')
    finished_requests = []

    def handle(self, *args, **options):
        count = 84
        failed_count = 0

        self.stdout.write(self.style.NOTICE(' %s | ----STARTING TV SHOWS----' % datetime.now()))

        while failed_count < 25:
            finished_requests = self.request_batch_tv_show(count)

            if len(finished_requests) == 0:
                failed_count += 1
            else:
                failed_count = 0
            count += 1

        self.stdout.write(self.style.SUCCESS(' %s | ----FINISHED IMPORTING-----' % datetime.now()))

    def request_batch_tv_show(self, initial_value=0, request_amount=2):
        requests = []
        for counter in range(0, request_amount):
            print((initial_value * request_amount) + counter, sep=' ', end=' | ', flush=True)
            requests.append(RequestThread(self.tmdb_api_key, (initial_value * request_amount) + counter))

        for request in requests:
            request.start()

        for request in requests:
            request.join()

        for request in requests:
            if not request.tv_show:
                requests.remove(request)

        time.sleep(10)
        return requests

    @transaction.atomic
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
