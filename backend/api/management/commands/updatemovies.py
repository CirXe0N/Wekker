import threading
import time
import math
from datetime import datetime, date, timedelta
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from django.db import transaction
from Wekker_API.utilities.env_reader import get_env
from api.management.tmdb.tmdb_controller import get_movie, get_image, get_movie_changes
from api.management.tmdb.tmdb_parser import parse_movie_data, parse_movie_sources_data, update_movie_data
from api.management.tmdb.tmdb_validator import validate_movie_data
from api.models import Person, Genre, MovieCastMember, MovieCrewMember, MovieSources


class Command(BaseCommand):
    help = 'Update Movies from TMDB'
    tmdb_api_key = get_env('TMDB_API_KEY')
    request_amount = 0
    results = []

    def add_arguments(self, parser):
        today = date.today()

        # Start date Value
        parser.add_argument(
            '--start',
            action='store',
            type=str,
            default=date.today(),
            dest='start_date',
            help='Start collecting process at the given date',
        )

        # End date Value
        parser.add_argument(
            '--end',
            action='store',
            type=str,
            default=today + timedelta(days=1),
            dest='end_date',
            help='Stop collecting process at the given date',
        )

    def handle(self, *args, **options):
        start_date = options.get('start_date')
        end_date = options.get('end_date')
        changes = get_movie_changes(self.tmdb_api_key, start_date=start_date, end_date=end_date)
        total_pages = changes['total_pages']
        self.manage_requests()

        for result in changes['results']:
            self.results.append(result)

        for page_number in range(2, total_pages + 1):
            print('Page %s' % page_number)
            changes = get_movie_changes(self.tmdb_api_key, start_date=start_date, end_date=end_date, page=page_number)
            self.manage_requests()

            for result in changes['results']:
                self.results.append(result)

        print('Total Movies: %s' % len(self.results))
        request_loop_amount = math.ceil(len(self.results) / 20)
        time.sleep(10)
        count = 0
        while count < request_loop_amount:
            self.request_batch_movie(initial_value=count, request_amount=20)
            count += 1

    def manage_requests(self):
        self.request_amount += 1
        if self.request_amount % 40 == 0:
            print('(%s) : WAITING 10 SEC' % datetime.now())
            time.sleep(10)

    @transaction.atomic
    def request_batch_movie(self, initial_value=0, request_amount=20):
        requests = []
        print('%s :  %s - %s' % (initial_value,
                                 (initial_value * request_amount),
                                 ((initial_value * request_amount) + request_amount)))

        for result in self.results[(initial_value * request_amount):(initial_value * request_amount) + request_amount]:
            requests.append(MovieRequestThread(self.tmdb_api_key, result['id']))

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
            print('(%s) : WAITING 10 SEC' % datetime.now())
            time.sleep(10)

        return requests

    @staticmethod
    def persist_movie(request):
        try:
            print('Update')
            sources = MovieSources.objects.get(tmdb_id=request.sources.tmdb_id)

            movie = sources.movie
            movie = update_movie_data(movie, request.movie)
            movie.save()

            if not sources.movie.poster and request.poster:
                sources.movie.poster.save('poster.jpg', request.poster)

            for genre in request.genres:
                if genre not in sources.movie.genres.all():
                    genre, created = Genre.objects.get_or_create(name=genre.name)
                    sources.movie.genres.add(genre)

            for genre in sources.movie.genres.all():
                if genre not in request.genres:
                    sources.movie.genres.remove(genre)

            for cast_member_data in request.cast_members:
                cast_members = MovieCastMember.objects.filter(movie=movie,
                                                              person__name=cast_member_data.person.name,
                                                              character=cast_member_data.character)

                if len(cast_members) == 0:
                    person, created = Person.objects.get_or_create(name=cast_member_data.person.name)
                    cast_member_data.person = person
                    cast_member_data.movie_id = request.media_count
                    cast_member_data.save()

            for cast_member in sources.movie.moviecastmember_set.all():
                if any(cast_member_data for cast_member_data in request.cast_members
                       if cast_member_data.person.name == cast_member.person.name
                       and cast_member_data.character == cast_member.character):
                    continue
                cast_member.delete()

            for crew_member_data in request.crew_members:
                crew_members = MovieCrewMember.objects.filter(movie=movie,
                                                              person__name=crew_member_data.person.name,
                                                              job_title=crew_member_data.job_title)

                if len(crew_members) == 0:
                    person, created = Person.objects.get_or_create(name=crew_member_data.person.name)
                    crew_member_data.person = person
                    crew_member_data.movie_id = request.media_count
                    crew_member_data.save()

                for crew_member in sources.movie.moviecrewmember_set.all():
                    if any(crew_member_data for crew_member_data in request.crew_members
                           if crew_member_data.person.name == crew_member.person.name
                           and crew_member_data.job_title == crew_member.job_title):
                        continue
                    crew_member.delete()

        except MovieSources.DoesNotExist:
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
                cast_member.movie_id = request.media_count

            for crew_member in request.crew_members:
                person, created = Person.objects.get_or_create(name=crew_member.person.name)
                crew_member.person = person
                crew_member.movie_id = request.media_count

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

            # if movie_data['poster_path']:
            #     self.poster = ContentFile(get_image('w185', movie_data['poster_path']).getvalue())

            for genre_data in movie_data['genres']:
                self.genres.append(Genre(name=genre_data.get('name')))

            for cast_member_data in movie_data['credits']['cast']:
                person = Person(name=cast_member_data['name'])

                if ' / ' in cast_member_data['character']:
                    for character_data in str.split(' / '):
                        cast_member = MovieCastMember(character=character_data, person=person,
                                                      movie_id=self.movie.id)
                        self.cast_members.append(cast_member)
                elif ', ' in cast_member_data['character']:
                    for character_data in str.split(', '):
                        cast_member = MovieCastMember(character=character_data, person=person,
                                                      movie_id=self.movie.id)
                        self.cast_members.append(cast_member)
                elif len(cast_member_data['character']) > 150:
                    pass
                else:
                    cast_member = MovieCastMember(character=cast_member_data['character'], person=person,
                                                  movie_id=self.movie.id)
                    self.cast_members.append(cast_member)

            for crew_member_data in movie_data['credits']['crew']:
                person = Person(name=crew_member_data['name'])
                crew_member = MovieCrewMember(job_title=crew_member_data['job'], person=person,
                                              movie_id=self.movie.id)
                self.crew_members.append(crew_member)
        return None
