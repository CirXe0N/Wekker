from celery.schedules import crontab
from celery.task import periodic_task
from celery.task import task
from celery.utils.log import get_task_logger
from django.core.management import call_command

from api.utilities import emails, reminders

logger = get_task_logger(__name__)


@periodic_task(run_every=crontab(minute=0, hour='*/1'), name="get_scheduled_tv_shows")
def get_scheduled_tv_shows_task():
    logger.info('Starting')
    reminders.get_scheduled_tv_shows()
    logger.info('Finished')


@periodic_task(run_every=crontab(minute=0, hour=0), name="get_scheduled_movies")
def get_scheduled_movies_task():
    logger.info('Starting')
    reminders.get_scheduled_movies()
    logger.info('Finished')


@task(name="send_tv_show_episode_reminder")
def send_tv_show_episode_reminder_task(email_address, episode_id):
    logger.info('Starting')
    emails.send_tv_show_reminder_email(email_address, episode_id)
    logger.info('Finished')


@task(name="send_movie_reminder")
def send_movie_reminder_task(email_address, movie_id):
    logger.info('Starting')
    emails.send_movie_reminder_email(email_address, movie_id)
    logger.info('Finished')


@periodic_task(run_every=crontab(minute=0, hour=6), name="update_tv_shows")
def update_tv_shows():
    logger.info('Starting')
    call_command('updatetvshows')
    logger.info('Finished')


@periodic_task(run_every=crontab(minute=0, hour=3), name="update_movies")
def update_movies():
    logger.info('Starting')
    call_command('updatemovies')
    logger.info('Finished')
