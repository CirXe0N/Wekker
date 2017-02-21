import threading
import time
from datetime import datetime
from dateutil.parser import parse
from django.core.management import BaseCommand
from django.db import transaction
from api.management.tvmaze.tvmaze_controller import get_tv_show_by_imdb, get_tv_show_episode
from api.models import TVShowEpisode, TVShowSources


class Command(BaseCommand):
    help = 'Collect TV Show Episode Airtime from TV Maze'
    request_amount = 0

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
            help='Collect air times for a single TV Show (Database TV Show ID)',
        )

    def handle(self, *args, **options):
        if options['initial']:
            self.stdout.write(self.style.NOTICE(' %s | ----STARTING TV SHOW EPISODE AIRTIME----' % datetime.now()))
            self.request_batch_tv_show_episode(TVShowSources.objects.filter(tv_show_id__gte=options['initial']))
            self.stdout.write(self.style.SUCCESS('%s | ----FINISHED IMPORTING-----' % datetime.now()))

        if options['single']:
            self.stdout.write(self.style.NOTICE('%s | ----GRAB AIR TIMES OF TV SHOW (%s) ----' %
                                                datetime.now(), options['single']))
            self.request_batch_tv_show_episode(TVShowSources.objects.filter(tv_show_id=options['single']))
            self.stdout.write(self.style.SUCCESS('%s | ----FINISHED IMPORTING-----' % datetime.now()))

    def manage_requests(self):
        self.request_amount += 1
        if self.request_amount % 20 == 0:
            time.sleep(11)

    @transaction.atomic
    def request_batch_tv_show_episode(self, sources):
        for source in sources:
            tv_maze_tv_show = get_tv_show_by_imdb(source.imdb_id)
            self.manage_requests()

            if tv_maze_tv_show and 'id' in tv_maze_tv_show:
                episodes = TVShowEpisode.objects.filter(season__tv_show=source.tv_show, air_date__isnull=True)

                for episode in episodes:
                    self.manage_requests()
                    TVShowEpisodeRequestThread(tv_maze_tv_show['id'], episode).start()

            print('(%s) : %s' % (datetime.now(), source.tv_show.name))


class TVShowEpisodeRequestThread(threading.Thread):
    def __init__(self, tv_maze_tv_show_id, episode):
        self.tv_maze_tv_show_id = tv_maze_tv_show_id
        self.episode = episode
        threading.Thread.__init__(self)

    def run(self):
        tv_maze_episode = get_tv_show_episode(self.tv_maze_tv_show_id, self.episode.season_number,
                                              self.episode.episode_number)
        if tv_maze_episode and 'airstamp' in tv_maze_episode:
            self.episode.air_date = parse(tv_maze_episode['airstamp'])
            self.episode.save()
