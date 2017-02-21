import threading
import time
from datetime import datetime
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from django.db import transaction
from Wekker_API.utilities.env_reader import get_env
from api.management.tmdb.tmdb_controller import get_tv_show, get_image
from api.management.tmdb.tmdb_parser import parse_tv_show_data, parse_tv_show_sources_data
from api.management.tmdb.tmdb_validator import validate_tv_show_data
from api.models import Person, Genre, TVShowCrewMember, TVShowCastMember


class Command(BaseCommand):
    help = 'Collect TV Shows from TMDB'
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

        # Import single TV Show
        parser.add_argument(
            '--single',
            action='store',
            type=int,
            default=None,
            dest='single',
            help='Collect a single TV Show by ID',
        )

    def handle(self, *args, **options):
        if options['initial'] is not None:
            self.stdout.write(self.style.NOTICE('%s | ----COLLECTING TV SHOWS----' % datetime.now()))
            count = options['initial']
            failed_count = 0
            while failed_count < 1000:
                finished_requests = self.request_batch_tv_show(initial_value=count, request_amount=20)

                for request in finished_requests:
                    if not request.tv_show:
                        failed_count += 1
                    else:
                        failed_count = 0

                count += 1
            self.stdout.write(self.style.SUCCESS('%s | ----FINISHED IMPORTING-----' % datetime.now()))

        if options['single']:
            self.stdout.write(self.style.NOTICE('%s | ----GRAB TV SHOW (%s)----' % datetime.now(), options['single']))
            self.request_batch_tv_show(initial_value=options['single'], request_amount=1)
            self.stdout.write(self.style.SUCCESS('%s | ----FINISHED IMPORTING-----' % datetime.now()))

    @transaction.atomic
    def request_batch_tv_show(self, initial_value=0, request_amount=20):
        requests = []
        for counter in range(0, request_amount):
            requests.append(TVShowRequestThread(self.tmdb_api_key, (initial_value * request_amount) + counter))

        for request in requests:
            request.start()

        for request in requests:
            request.join()

        for request in requests:
            if not request.tv_show:
                requests.remove(request)
            else:
                self.persist_tv_show(request)
                print('(%s) : %s' % (datetime.now(), request.tv_show.name))

        if request_amount != 1:
            time.sleep(10)

        return requests

    @staticmethod
    def persist_tv_show(request):
        request.tv_show.save()
        request.sources.save()

        if request.poster:
            request.tv_show.poster.save('poster.jpg', request.poster)

        for genre in request.genres:
            genre, created = Genre.objects.get_or_create(name=genre.name)
            request.tv_show.genres.add(genre)

        for cast_member in request.cast_members:
            person, created = Person.objects.get_or_create(name=cast_member.person.name)
            cast_member.person = person

        for crew_member in request.crew_members:
            person, created = Person.objects.get_or_create(name=crew_member.person.name)
            crew_member.person = person

        TVShowCastMember.objects.bulk_create(request.cast_members)
        TVShowCrewMember.objects.bulk_create(request.crew_members)


class TVShowRequestThread(threading.Thread):
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
        self.sources = None
        self.error_message = None
        threading.Thread.__init__(self)

    def run(self):
        tv_show_data = get_tv_show(self.tmdb_api_key, self.media_count)
        valid, self.error_message = validate_tv_show_data(tv_show_data)

        if valid:
            self.tv_show = parse_tv_show_data(self.media_count, tv_show_data)
            self.sources = parse_tv_show_sources_data(self.tv_show, tv_show_data['external_ids'])

            if tv_show_data['poster_path']:
                self.poster = ContentFile(get_image('w185', tv_show_data['poster_path']).getvalue())

            for genre_data in tv_show_data['genres']:
                self.genres.append(Genre(name=genre_data.get('name')))

            for cast_member_data in tv_show_data['credits']['cast']:
                person = Person(name=cast_member_data['name'])
                cast_member = TVShowCastMember(character=cast_member_data['character'], person=person)
                self.cast_members.append(cast_member)

            for creator_data in tv_show_data['created_by']:
                person = Person(name=creator_data['name'])
                crew_member = TVShowCrewMember(job_title='Creator', person=person, tv_show_id=self.tv_show.id)
                self.crew_members.append(crew_member)

            for crew_member_data in tv_show_data['credits']['crew']:
                person = Person(name=crew_member_data['name'])
                crew_member = TVShowCrewMember(job_title=crew_member_data['job'], person=person,
                                               tv_show_id=self.tv_show.id)
                self.crew_members.append(crew_member)
