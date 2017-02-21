import threading
import time
from datetime import datetime
from django.core.management import BaseCommand
from django.db import transaction
from Wekker_API.utilities.env_reader import get_env
from api.management.tmdb.tmdb_controller import get_tv_show_season
from api.management.tmdb.tmdb_parser import parse_tv_show_season_data, parse_tv_show_episodes_data
from api.models import TVShowEpisode, TVShowSources


class Command(BaseCommand):
    help = 'Collect TV Show Seasons from TMDB'
    tmdb_api_key = get_env('TMDB_API_KEY')

    def add_arguments(self, parser):
        # Initial Value
        parser.add_argument(
            '--initial',
            action='store',
            type=int,
            default=0,
            dest='initial',
            help='Start collecting process at the given database TV SHOW ID',
        )

        # Import single TV Show
        parser.add_argument(
            '--single',
            action='store',
            type=int,
            default=None,
            dest='single',
            help='Collect a seasons for a single TV Show (Database TV Show ID)',
        )

    def handle(self, *args, **options):
        if options['initial']:
            self.stdout.write(self.style.NOTICE(' %s | ----STARTING TV SHOWS SEASONS----' % datetime.now()))
            self.request_batch_tv_show_season(TVShowSources.objects.filter(tv_show_id__gte=options['initial']))
            self.stdout.write(self.style.SUCCESS('%s | ----FINISHED IMPORTING-----' % datetime.now()))

        if options['single']:
            self.stdout.write(self.style.NOTICE('%s | ----GRAB SEASONS OF TV SHOW (%s) ----' %
                                                datetime.now(), options['single']))
            self.request_batch_tv_show_season(TVShowSources.objects.filter(tv_show_id=options['single']))
            self.stdout.write(self.style.SUCCESS('%s | ----FINISHED IMPORTING-----' % datetime.now()))

    def request_batch_tv_show_season(self, sources):
        requests = []
        request_count = 0

        for source in sources:
            tv_show = source.tv_show

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

            requests = []

    @staticmethod
    @transaction.atomic
    def persist_tv_show_season(requests):
        for request in requests:
            if request.season:
                season = request.season
                season.save()

                for episode in request.episodes:
                    episode.season = season

                    if not episode.season_number:
                        episode.season_number = season.season_number

                TVShowEpisode.objects.bulk_create(request.episodes)


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
