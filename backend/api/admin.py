from django.contrib import admin
from api.models import UserProfile, TVShow, Genre, Person, Movie, MovieSources, TVShowSeason, TVShowEpisode


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name',)
    exclude = ('tv_shows', 'movies', 'movies_watched',)

    @staticmethod
    def first_name(obj):
        return obj.user.first_name

    @staticmethod
    def last_name(obj):
        return obj.user.last_name


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TVShow)
class TVShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'first_air_date', 'status', 'season_count', 'episode_count',)


@admin.register(TVShowSeason)
class TVShowSeasonAdmin(admin.ModelAdmin):
    list_display = ('tv_show', 'season_number', 'episode_count',)
    search_fields = ['tv_show__name']


@admin.register(TVShowEpisode)
class TVShowEpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'season_number', 'episode_number',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date', 'status',)


@admin.register(MovieSources)
class MovieSourcesAdmin(admin.ModelAdmin):
    list_display = ('movie',)
