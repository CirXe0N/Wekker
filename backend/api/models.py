import uuid
from django.contrib.auth.models import User
from django.db import models


""" USERS """


def user_profile_photo_directory_path(instance, filename):
    return "users/%s/profile_photos/%s" % (instance.profile_id, filename)


class UserProfile(models.Model):
    profile_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    photo = models.ImageField(upload_to=user_profile_photo_directory_path, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    password_recovery_at = models.DateTimeField(blank=True, null=True)
    password_recovery_token = models.UUIDField(default=uuid.uuid4, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tv_shows = models.ManyToManyField('TVShow', related_name='collectors')
    movies = models.ManyToManyField('Movie', related_name='collectors')
    movies_watched = models.ManyToManyField('Movie', related_name='watchers')

    def __str__(self):
        return self.user.email


""" MEDIA GENERAL """


class Genre(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


""" TV SHOWS """


def tv_show_backdrop_directory_path(instance, filename):
    return "tv_shows/%s/backdrop/%s" % (instance.tv_show_id, filename)


def tv_show_poster_directory_path(instance, filename):
    return "tv_shows/%s/poster/%s" % (instance.tv_show_id, filename)


class TVShow(models.Model):
    tv_show_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    overview = models.TextField(null=True)
    type = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    first_air_date = models.DateField(null=True)
    in_production = models.BooleanField(default=False)
    original_language = models.CharField(max_length=50, null=True, blank=True)
    origin_country = models.CharField(max_length=75, null=True, blank=True)
    episode_count = models.IntegerField(null=True)
    season_count = models.IntegerField(null=True)
    poster = models.ImageField(upload_to=tv_show_poster_directory_path, null=True)
    cast = models.ManyToManyField(Person, through='TVShowCastMember', related_name='tv_show_cast_member')
    crew = models.ManyToManyField(Person, through='TVShowCrewMember', related_name='tv_show_crew_member')
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name

    def is_user_collection_item(self, request):
        profile = UserProfile.objects.get(request.user)
        return bool(self.watchers.filter(profile_id=profile.profile_id))


class TVShowCastMember(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)
    character = models.CharField(max_length=150, blank=True, null=True)


class TVShowCrewMember(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=150, blank=True, null=True)


class TVShowSources(models.Model):
    tv_show = models.OneToOneField(TVShow, on_delete=models.CASCADE)
    tmdb_id = models.CharField(max_length=50, null=True)
    imdb_id = models.CharField(max_length=50, null=True)
    freebase_id = models.CharField(max_length=50, null=True)
    tvdb_id = models.CharField(max_length=50, null=True)
    tvrage_id = models.CharField(max_length=50, null=True)


class TVShowSeason(models.Model):
    tv_show = models.ForeignKey(TVShow, related_name='seasons', on_delete=models.CASCADE)
    season_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    season_number = models.IntegerField()
    episode_count = models.IntegerField(null=True)


class TVShowEpisode(models.Model):
    season = models.ForeignKey(TVShowSeason, related_name='episodes', on_delete=models.CASCADE)
    episode_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=255, null=True)
    overview = models.TextField(null=True, blank=True)
    air_date = models.DateTimeField(null=True, blank=True)
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    watchers = models.ManyToManyField(UserProfile)


""" MOVIES """


def movie_poster_directory_path(instance, filename):
    return "movies/%s/poster/%s" % (instance.movie_id, filename)


class Movie(models.Model):
    movie_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    overview = models.TextField(null=True)
    status = models.CharField(max_length=50, null=True)
    release_date = models.DateField(null=True)
    original_language = models.CharField(max_length=50, null=True, blank=True)
    poster = models.ImageField(upload_to=movie_poster_directory_path, null=True)
    runtime = models.IntegerField()
    cast = models.ManyToManyField(Person, through='MovieCastMember', related_name='movie_cast_members')
    crew = models.ManyToManyField(Person, through='MovieCrewMember', related_name='movie_crew_members')
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name

    def is_user_collection_item(self, request):
        profile = UserProfile.objects.get(request.user)
        return bool(self.watchers.filter(profile_id=profile.profile_id))


class MovieCastMember(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    character = models.CharField(max_length=150, blank=True, null=True)


class MovieCrewMember(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=150, blank=True, null=True)


class MovieSources(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    tmdb_id = models.CharField(max_length=50, null=True)
    imdb_id = models.CharField(max_length=50, blank=True, null=True)
