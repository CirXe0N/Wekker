import threading
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from Wekker_API.utilities.env_reader import get_env
from api.models import UserProfile, TVShowEpisode, TVShow, Movie


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, email_sender, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.email_sender = email_sender
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, self.email_sender, self.recipient_list)
        msg.content_subtype = 'html'
        msg.send()


def send_reset_password_email(recipient):
    subject = 'Reset Wekker Password'
    sender = 'Wekker <%s>' % get_env('EMAIL_USER')

    try:
        user = User.objects.get(email=recipient)
        profile = UserProfile.objects.get(user=user)
        profile.password_recovery_at = timezone.now()
        profile.password_recovery_token = uuid.uuid4()
        profile.save()

        url = '%s/account-recovery/%s' % (get_env('FRONTEND_URL'), profile.password_recovery_token)
        html_content = render_to_string('../templates/emails/reset_password.html', {'url': url})
        EmailThread(subject, html_content, sender, [recipient]).start()
    except User.DoesNotExist or UserProfile.DoesNotExist:
        pass


def send_account_verification_email(recipient):
    subject = 'Wekker Account Verification'
    sender = 'Wekker <%s>' % get_env('EMAIL_USER')

    try:
        user = User.objects.get(email=recipient)
        profile = UserProfile.objects.get(user=user)
        url = '%s/account-verification/%s' % (get_env('FRONTEND_URL'), profile.profile_id)
        html_content = render_to_string('../templates/emails/verify_account.html', {'url': url})
        EmailThread(subject, html_content, sender, [recipient]).start()
    except User.DoesNotExist or UserProfile.DoesNotExist:
        pass


def send_feedback_email(user, message, feedback_type):
    subject = '[WEKKER] Feedback from %s %s' % (user.first_name, user.last_name)
    sender = 'Wekker Feedback <%s>' % get_env('EMAIL_USER')
    recipient = get_env('EMAIL_FEEDBACK')
    html_content = render_to_string('../templates/emails/feedback.html', {'user': user, 'feedback_type': feedback_type,
                                                                          'message': message})
    msg = EmailMessage(subject, html_content, sender, [recipient])
    msg.send()


def send_recommendation_email(user, recipient, media_type, media):
    subject = '%s Recommendation from %s %s' % (media_type, user.first_name, user.last_name)
    sender = 'Wekker <%s>' % get_env('EMAIL_USER')
    if media_type == 'TV Show':
        url = '%s/main/tv-shows/%s' % (get_env('FRONTEND_URL'), media.tv_show_id)
    else:
        url = '%s/main/movies/%s' % (get_env('FRONTEND_URL'), media.movie_id)

    html_content = render_to_string('../templates/emails/recommendation.html', {'user': user, 'media': media,
                                                                                'url': url, 'media_type': media_type})
    msg = EmailMessage(subject, html_content, sender, [recipient])
    msg.content_subtype = 'html'
    msg.send()


def send_tv_show_reminder_email(recipient, episode_id):
    episode = TVShowEpisode.objects.get(episode_id=episode_id)
    tv_show = TVShow.objects.get(seasons__episodes=episode)
    subject = 'Reminder: New "%s" Episode (S%s E%s) in a hour' % (tv_show.name, episode.season_number, episode.episode_number)
    url = '%s/main/tv-shows/%s' % (get_env('FRONTEND_URL'), tv_show.tv_show_id)
    sender = 'Wekker <%s>' % get_env('EMAIL_USER')

    html_content = render_to_string('../templates/emails/tv_show_episode_reminder.html', {'tv_show': tv_show,
                                                                                          'episode': episode,
                                                                                          'url': url})
    msg = EmailMessage(subject, html_content, sender, [recipient])
    msg.content_subtype = 'html'
    msg.send()


def send_movie_reminder_email(recipient, movie_id):
    movie = Movie.objects.get(movie_id=movie_id)
    subject = 'Reminder: "%s" will be released tomorrow.' % movie.name
    url = '%s/main/movies/%s' % (get_env('FRONTEND_URL'), movie.movie_id)
    sender = 'Wekker <%s>' % get_env('EMAIL_USER')

    html_content = render_to_string('../templates/emails/movie_reminder.html', {'movie': movie, 'url': url})
    msg = EmailMessage(subject, html_content, sender, [recipient])
    msg.content_subtype = 'html'
    msg.send()
