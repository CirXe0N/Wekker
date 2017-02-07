from datetime import datetime, timedelta
from django.utils import timezone
from api import tasks
from api.models import TVShowEpisode, TVShow, Movie


def get_scheduled_tv_shows():
    now = timezone.now()
    tv_show_episodes = TVShowEpisode.objects.filter(air_date__range=(now, now + timedelta(hours=1)))

    tv_shows_sent = []
    for episode in tv_show_episodes:
        tv_show = TVShow.objects.get(seasons__episodes=episode)

        if tv_show not in tv_shows_sent:
            for collector in tv_show.collectors.all():
                tasks.send_tv_show_episode_reminder_task(collector.user.email, episode.episode_id)
            tv_shows_sent.append(tv_show)


def get_scheduled_movies():
    today = datetime.today()
    movies = Movie.objects.filter(release_date=today + timedelta(days=1))
    for movie in movies:
        for collector in movie.collectors.all():
            tasks.send_movie_reminder_task(collector.user.email, movie.movie_id)
