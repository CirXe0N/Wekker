import threading
import time
from datetime import datetime
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from django.db import transaction
from Wekker_API.utilities.env_reader import get_env
from api.management.tmdb.tmdb_controller import get_movie, get_image
from api.management.tmdb.tmdb_parser import parse_movie_data, parse_movie_sources_data
from api.management.tmdb.tmdb_validator import validate_movie_data
from api.models import Person, Genre, MovieCastMember, MovieCrewMember


class Command(BaseCommand):
    help = 'Collect Movies from TMDB'
    tmdb_api_key = get_env('TMDB_API_KEY')
    finished_requests = []

    def add_arguments(self, parser):
        # Initial Value
        parser.add_argument(
            '--initial',
            action='store',
            type=int,
            default=None,
            dest='initial',
            help='Start collecting process at the given batch number',
        )

        # Import single Movie
        parser.add_argument(
            '--single',
            action='store',
            type=int,
            default=None,
            dest='single',
            help='Collect a single Movie by ID',
        )

    def handle(self, *args, **options):
        if options['initial'] is not None:
            self.stdout.write(self.style.NOTICE('%s | ----COLLECTING MOVIES----' % datetime.now()))
            count = options['initial']
            failed_count = 0
            while failed_count < 1000:
                finished_requests = self.request_batch_movie(initial_value=count, request_amount=20)

                for request in finished_requests:
                    if not request.movie:
                        failed_count += 1
                    else:
                        failed_count = 0

                count += 1

            self.stdout.write(self.style.SUCCESS('%s | ----FINISHED IMPORTING-----' % datetime.now()))

        if options['single']:
            self.stdout.write(self.style.NOTICE('%s | ----GRAB MOVIE (%s)----' % (datetime.now(), options['single'])))
            self.request_batch_movie(initial_value=options['single'], request_amount=1)
            self.stdout.write(self.style.SUCCESS('%s | ----FINISHED IMPORTING-----' % datetime.now()))

    @transaction.atomic
    def request_batch_movie(self, initial_value=0, request_amount=20):
        requests = []
        for counter in range(0, request_amount):
            requests.append(MovieRequestThread(self.tmdb_api_key, (initial_value * request_amount) + counter))

        for request in requests:
            request.start()

        for request in requests:
            request.join()

        for request in requests:
            if not request.movie:
                requests.remove(request)
            else:
                self.persist_movie(request)
                print('(%s) : (%s) %s' % (datetime.now(), request.movie.id, request.movie.name))

        if request_amount != 1:
            time.sleep(10)

        return requests

    @staticmethod
    def persist_movie(request):
        request.movie.save()
        request.sources.save()

        if request.poster:
            request.movie.poster.save('poster.jpg', request.poster)

        for genre in request.genres:
            genre, created = Genre.objects.get_or_create(name=genre.name)
            request.movie.genres.add(genre)

        for cast_member in request.cast_members:
            person, created = Person.objects.get_or_create(name=cast_member.person.name)
            cast_member.person = person

        for crew_member in request.crew_members:
            person, created = Person.objects.get_or_create(name=crew_member.person.name)
            crew_member.person = person

        MovieCastMember.objects.bulk_create(request.cast_members)
        MovieCrewMember.objects.bulk_create(request.crew_members)


class MovieRequestThread(threading.Thread):
    def __init__(self, tmdb_api_key, media_count):
        self.tmdb_api_key = tmdb_api_key
        self.media_count = media_count
        self.error_message = None
        self.movie = None
        self.poster = None
        self.genres = []
        self.cast_members = []
        self.crew_members = []
        self.sources = None
        threading.Thread.__init__(self)

    def run(self):
        movie_data = get_movie(self.tmdb_api_key, self.media_count)
        valid, error_message = validate_movie_data(movie_data)

        if valid:
            self.movie = parse_movie_data(self.media_count, movie_data)
            self.sources = parse_movie_sources_data(self.movie, movie_data)

            if movie_data['poster_path']:
                self.poster = ContentFile(get_image('w185', movie_data['poster_path']).getvalue())

            for genre_data in movie_data['genres']:
                self.genres.append(Genre(name=genre_data.get('name')))

            for cast_member_data in movie_data['credits']['cast']:
                person = Person(name=cast_member_data['name'])

                if ' / ' in cast_member_data['character']:
                    for character_data in str.split(' / '):
                        cast_member = MovieCastMember(character=character_data, person=person, movie_id=self.movie.id)
                        self.cast_members.append(cast_member)
                elif ', ' in cast_member_data['character']:
                    for character_data in str.split(', '):
                        cast_member = MovieCastMember(character=character_data, person=person, movie_id=self.movie.id)
                        self.cast_members.append(cast_member)
                elif len(cast_member_data['character']) > 150:
                    pass
                else:
                    cast_member = MovieCastMember(character=cast_member_data['character'], person=person,
                                                  movie_id=self.movie.id)
                    self.cast_members.append(cast_member)

            for crew_member_data in movie_data['credits']['crew']:
                person = Person(name=crew_member_data['name'])
                crew_member = MovieCrewMember(job_title=crew_member_data['job'], person=person, movie_id=self.movie.id)
                self.crew_members.append(crew_member)
