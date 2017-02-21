import threading
import time
import math
from datetime import datetime, date, timedelta
from dateutil.parser import parse
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from django.db import transaction
from Wekker_API.utilities.env_reader import get_env
from api.management.tmdb.tmdb_controller import get_tv_show_changes, get_tv_show, get_image, get_tv_show_season
from api.management.tmdb.tmdb_parser import parse_tv_show_data, parse_tv_show_sources_data, update_tv_show_data, \
    parse_tv_show_season_data, parse_tv_show_episodes_data, update_tv_show_season_data, update_tv_show_episodes_data
from api.management.tmdb.tmdb_validator import validate_tv_show_data
from api.management.tvmaze.tvmaze_controller import get_tv_show_by_imdb, get_tv_show_episode
from api.models import Person, Genre, TVShowCrewMember, TVShowCastMember, TVShow, TVShowSources, TVShowSeason, \
    TVShowEpisode


class Command(BaseCommand):
    help = 'Update TV Shows from TMDB'
    tmdb_api_key = get_env('TMDB_API_KEY')
    request_amount = 0
    results = []
    updated_tv_shows = []

    def add_arguments(self, parser):
        today = date.today()

        # Start date Value
        parser.add_argument(
            '--start',
            action='store',
            type=str,
            default=today,
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
        changes = get_tv_show_changes(self.tmdb_api_key, start_date=start_date, end_date=end_date)
        total_pages = changes['total_pages']
        self.manage_requests()

        for result in changes['results']:
            self.results.append(result)

        for page_number in range(2, total_pages + 1):
            changes = get_tv_show_changes(self.tmdb_api_key, start_date=start_date, end_date=end_date, page=page_number)
            self.manage_requests()

            for result in changes['results']:
                self.results.append(result)

        print('Total TV Shows: %s' % len(self.results))
        request_loop_amount = math.ceil(len(self.results) / 20)
        time.sleep(10)
        count = 0
        while count < request_loop_amount:
            finished_requests = self.request_batch_tv_show(initial_value=count, request_amount=20)

            for finished_request in finished_requests:
                self.updated_tv_shows.append(finished_request.tv_show)
            count += 1

        self.request_batch_tv_show_season(self.updated_tv_shows)
        self.request_batch_tv_show_episode(self.updated_tv_shows)

    @transaction.atomic
    def request_batch_tv_show(self, initial_value=0, request_amount=20):
        requests = []
        finished_requests = []
        print('%s :  %s - %s' % (initial_value,
                                 (initial_value * request_amount),
                                 ((initial_value * request_amount) + request_amount)))

        for result in self.results[(initial_value * request_amount):(initial_value * request_amount) + request_amount]:
            requests.append(TVShowRequestThread(self.tmdb_api_key, result['id']))

        for request in requests:
            request.start()

        for request in requests:
            request.join()

        for request in requests:
            if not request.tv_show:
                requests.remove(request)
            else:
                self.persist_tv_show(request)
                finished_requests.append(request)
                print('(%s) : %s' % (datetime.now(), request.tv_show.name))

        if request_amount != 1:
            time.sleep(10)
        return finished_requests

    def request_batch_tv_show_season(self, tv_shows):
        requests = []
        request_count = 0

        for tv_show in tv_shows:

            try:
                source = TVShowSources.objects.get(tv_show=tv_show)

                for season_number in range(1, tv_show.season_count + 1):
                    request = TVShowSeasonRequestThread(self.tmdb_api_key, season_number, source, tv_show)
                    request.start()
                    request_count += 1
                    requests.append(request)

                    if request_count > 15:
                        time.sleep(10)
                        request_count = 0

                    print('(%s) : %s : SEASON %s' % (datetime.now(), tv_show.name, season_number))

                for request in requests:
                    request.join()

                self.persist_tv_show_season(requests)

            except TVShowSources.DoesNotExist:
                print('(%s) : (%s) NOT FOUND' % (datetime.now(), tv_show.id))

            requests = []

    @transaction.atomic
    def request_batch_tv_show_episode(self, tv_shows):
        for tv_show in tv_shows:
            source = TVShowSources.objects.get(tv_show=tv_show)
            tv_maze_tv_show = get_tv_show_by_imdb(source.imdb_id)
            self.manage_requests_tv_maze()

            if tv_maze_tv_show and 'id' in tv_maze_tv_show:
                episodes = TVShowEpisode.objects.filter(season__tv_show=tv_show, air_date__isnull=True)

                for episode in episodes:
                    self.manage_requests_tv_maze()
                    TVShowEpisodeRequestThread(tv_maze_tv_show['id'], episode).start()
                    print('(%s) : %s - %s - %s' % (datetime.now(), source.tv_show.name, episode.season_number,
                                                   episode.episode_number))

    def manage_requests(self):
        self.request_amount += 1
        if self.request_amount % 40 == 0:
            print('(%s) : WAITING 10 SEC' % datetime.now())
            time.sleep(10)

    def manage_requests_tv_maze(self):
        self.request_amount += 1
        if self.request_amount % 20 == 0:
            print('(%s) : WAITING 11 SEC' % datetime.now())
            time.sleep(11)

    @staticmethod
    def persist_tv_show(request):
        try:
            sources = TVShowSources.objects.get(tmdb_id=request.sources.tmdb_id)

            tv_show = sources.tv_show
            tv_show = update_tv_show_data(tv_show, request.tv_show)
            tv_show.save()

            if not sources.tv_show.poster and request.poster:
                sources.tv_show.poster.save('poster.jpg', request.poster)

            for genre in request.genres:
                if genre not in sources.tv_show.genres.all():
                    genre, created = Genre.objects.get_or_create(name=genre.name)
                    sources.tv_show.genres.add(genre)

            for genre in sources.tv_show.genres.all():
                if genre not in request.genres:
                    sources.tv_show.genres.remove(genre)

            for cast_member_data in request.cast_members:
                cast_members = TVShowCastMember.objects.filter(tv_show=tv_show,
                                                               person__name=cast_member_data.person.name,
                                                               character=cast_member_data.character)

                if len(cast_members) == 0:
                    person, created = Person.objects.get_or_create(name=cast_member_data.person.name)
                    cast_member_data.person = person
                    cast_member_data.tv_show_id = request.media_count
                    cast_member_data.save()

            for cast_member in sources.tv_show.tvshowcastmember_set.all():
                if any(cast_member_data for cast_member_data in request.cast_members
                       if cast_member_data.person.name == cast_member.person.name
                       and cast_member_data.character == cast_member.character):
                    continue
                cast_member.delete()

            for crew_member_data in request.crew_members:
                crew_members = TVShowCrewMember.objects.filter(tv_show=tv_show,
                                                               person__name=crew_member_data.person.name,
                                                               job_title=crew_member_data.job_title)

                if len(crew_members) == 0:
                    person, created = Person.objects.get_or_create(name=crew_member_data.person.name)
                    crew_member_data.person = person
                    crew_member_data.tv_show_id = request.media_count
                    crew_member_data.save()

            for crew_member in sources.tv_show.tvshowcrewmember_set.all():
                if any(crew_member_data for crew_member_data in request.crew_members
                       if crew_member_data.person.name == crew_member.person.name
                       and crew_member_data.job_title == crew_member.job_title):
                    continue
                crew_member.delete()

        except TVShowSources.DoesNotExist:
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
                cast_member.tv_show_id = request.media_count

            for crew_member in request.crew_members:
                person, created = Person.objects.get_or_create(name=crew_member.person.name)
                crew_member.person = person
                crew_member.tv_show_id = request.media_count

            TVShowCastMember.objects.bulk_create(request.cast_members)
            TVShowCrewMember.objects.bulk_create(request.crew_members)

    @staticmethod
    @transaction.atomic
    def persist_tv_show_season(requests):
        for request in requests:
            if request.season:
                try:
                    season_data = request.season
                    season = TVShowSeason.objects.get(tv_show=request.tv_show, season_number=request.season_number)
                    season = update_tv_show_season_data(season, season_data)
                    season.save()

                    for episode_data in request.episodes:
                        try:
                            episode = TVShowEpisode.objects.get(season=season,
                                                                episode_number=episode_data.episode_number)
                            episode = update_tv_show_episodes_data(episode, episode_data)
                            if not episode.season_number:
                                episode.season_number = season.season_number
                            episode.save()

                        except TVShowEpisode.DoesNotExist:
                            episode_data.season = season
                            if not episode.season_number:
                                episode.season_number = season.season_number
                            episode_data.save()

                except TVShowSeason.DoesNotExist:
                    season = request.season
                    season.save()

                    for episode in request.episodes:
                        episode.season = season

                        if not episode.season_number:
                            episode.season_number = season.season_number

                    TVShowEpisode.objects.bulk_create(request.episodes)


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
                crew_member = TVShowCrewMember(job_title='Creator', person=person,
                                               tv_show_id=self.tv_show.id)
                self.crew_members.append(crew_member)

            for crew_member_data in tv_show_data['credits']['crew']:
                person = Person(name=crew_member_data['name'])
                crew_member = TVShowCrewMember(job_title=crew_member_data['job'], person=person,
                                               tv_show_id=self.tv_show.id)
                self.crew_members.append(crew_member)


class TVShowSeasonRequestThread(threading.Thread):
    def __init__(self, tmdb_api_key, season_number, source, tv_show):
        self.tmdb_api_key = tmdb_api_key
        self.season_number = season_number
        self.source = source
        self.tv_show = tv_show
        self.season = None
        self.episodes = []
        threading.Thread.__init__(self)

    def run(self):
        season_data = get_tv_show_season(self.tmdb_api_key, self.source.tmdb_id, self.season_number)
        if season_data:
            self.season = parse_tv_show_season_data(self.tv_show, season_data)

            for episode_data in season_data['episodes']:
                episode = parse_tv_show_episodes_data(self.season, episode_data)
                self.episodes.append(episode)


class TVShowEpisodeRequestThread(threading.Thread):
    def __init__(self, tv_maze_tv_show_id, episode):
        self.tv_maze_tv_show_id = tv_maze_tv_show_id
        self.episode = episode
        threading.Thread.__init__(self)

    def run(self):
        tv_maze_episode = get_tv_show_episode(self.tv_maze_tv_show_id, self.episode.season_number,
                                              self.episode.episode_number)
        if tv_maze_episode and 'airstamp' in tv_maze_episode:
            if tv_maze_episode['airstamp']:
                self.episode.air_date = parse(tv_maze_episode['airstamp'])
                self.episode.save()
