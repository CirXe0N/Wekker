import base64
from django.utils import timezone
from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from api.models import UserProfile, TVShow, TVShowCastMember, TVShowCrewMember, Genre, TVShowSources, Person, \
    TVShowSeason, TVShowEpisode, MovieSources, Movie, MovieCrewMember, MovieCastMember


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TVShowEpisodeSerializer(serializers.ModelSerializer):
    is_watched = serializers.SerializerMethodField()

    class Meta:
        model = TVShowEpisode
        exclude = ('id', 'season', 'watchers',)

    def get_is_watched(self, instance):
        profile = self.context.get("profile")
        return bool(instance.watchers.filter(profile_id=profile.profile_id))

    def update(self, instance, validated_data):
        profile = self.context.get("profile")
        is_watched = self.initial_data.get("is_watched")
        if is_watched:
            instance.watchers.add(profile)
        else:
            instance.watchers.remove(profile)
        return instance


class TVShowSeasonSerializer(serializers.ModelSerializer):
    episodes = TVShowEpisodeSerializer(many=True)

    class Meta:
        model = TVShowSeason
        exclude = ('id', 'tv_show',)


class TVShowCollectionSerializer(serializers.ModelSerializer):
    last_seen_episode = serializers.SerializerMethodField(read_only=True)
    last_released_episode = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TVShow
        fields = ('tv_show_id', 'poster', 'name', 'status', 'last_seen_episode', 'last_released_episode',)

    def get_last_seen_episode(self, obj):
        profile = self.context.get("profile", None)
        if not profile:
            return None

        episode = TVShowEpisode.objects.filter(watchers=profile, season__tv_show=obj).last()
        if not episode:
            return None

        return {
            "season_number": episode.season_number,
            "episode_number": episode.episode_number
        }

    def get_last_released_episode(self, obj):
        start_date = timezone.now()
        episode = TVShowEpisode.objects.filter(season__tv_show=obj,
                                               air_date__lte=start_date).last()
        if not episode:
            return None

        return {
            "season_number": episode.season_number,
            "episode_number": episode.episode_number
        }


class TVShowSearchSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    order = serializers.CharField(read_only=True)

    class Meta:
        model = TVShow
        fields = ('tv_show_id', 'name', 'first_air_date', 'type', 'order',)

    def get_type(self, obj):
        return 'TV Show'


class MovieSearchSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    order = serializers.CharField(read_only=True)

    class Meta:
        model = Movie
        fields = ('movie_id', 'name', 'release_date', 'type', 'order',)

    def get_type(self, obj):
        return 'Movie'


class TVShowCastMemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='person.name')

    class Meta:
        model = TVShowCastMember
        fields = ('name', 'character',)


class TVShowCrewMemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='person.name')

    class Meta:
        model = TVShowCrewMember
        fields = ('name', 'job_title',)


class TVShowDetailsSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    seasons = TVShowSeasonSerializer(many=True)
    cast = TVShowCastMemberSerializer(source='tvshowcastmember_set', read_only=True, many=True)
    crew = TVShowCrewMemberSerializer(source='tvshowcrewmember_set', read_only=True, many=True)
    is_collection_item = serializers.SerializerMethodField()

    class Meta:
        model = TVShow
        exclude = ('id', 'in_production',)

    def get_is_collection_item(self, obj):
        profile = self.context.get("profile")
        return bool(profile.tv_shows.filter(tv_show_id=obj.tv_show_id))

    def update(self, instance, validated_data):
        profile = self.context.get("profile")
        is_collection_item = self.initial_data.get("is_collection_item")

        if is_collection_item:
            profile.tv_shows.add(instance)
        else:
            profile.tv_shows.remove(instance)
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email_address = serializers.CharField(source='user.email')
    password = serializers.CharField(source='user.password', write_only=True)
    access_token = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        exclude = ('id', 'password_recovery_at', 'tv_shows', 'movies', 'movies_watched',)
        extra_kwargs = {
            'user': {'write_only': True},
            'photo': {'read_only': True},
        }

    def get_access_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj.user)
        return token.key

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        # Validate E-mail Address
        try:
            User.objects.get(email=user_data['email'])
            raise serializers.ValidationError({"email_address": ["This email is already registered."]})
        except User.DoesNotExist:
            pass

        # Create User
        user = User.objects.create_user(
            username=user_data['email'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )

        # # Create User Profile
        profile = UserProfile.objects.create(user=user)

        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.get('user', {})

        # Validate E-mail Address
        if user_data:
            if instance.user.email != user_data.get('email', ''):
                try:
                    User.objects.get(email=user_data.get('email', ''))
                    raise serializers.ValidationError({"email_address": ["This field must be unique."]})
                except User.DoesNotExist:
                    pass

        # Update User
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)

        if len(user_data.get('password')) > 4:
            user.set_password(user_data.get('password'))
        user.save()

        # Update User Profile
        profile_photo = self.initial_data.get('photo', '')
        profile_photo_name = self.initial_data.get('photo_name', '')
        profile_photo = profile_photo.split('base64,', 1)

        if len(profile_photo) > 1 and profile_photo_name:
            im = Image.open(BytesIO(base64.b64decode(profile_photo[1])))
            im.thumbnail((225, 225))
            outbuffer = BytesIO()
            im.save(outbuffer, format=im.format)
            instance.photo = ContentFile(outbuffer.getvalue(), profile_photo_name)

        instance.is_verified = validated_data.get('is_verified', instance.is_verified)
        instance.save()

        # Get Token
        token = Token.objects.get(user=user)
        instance.access_token = token

        return instance


class MovieCastMemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='person.name')

    class Meta:
        model = MovieCastMember
        fields = ('name', 'character',)


class MovieCrewMemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='person.name')

    class Meta:
        model = MovieCrewMember
        fields = ('name', 'job_title',)


class MovieSourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSources
        exclude = ('id',)


class MovieDetailsSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    sources = MovieSourcesSerializer(write_only=True)
    cast = MovieCastMemberSerializer(source='moviecastmember_set', read_only=True, many=True)
    crew = MovieCrewMemberSerializer(source='moviecrewmember_set', read_only=True, many=True)
    is_collection_item = serializers.SerializerMethodField()
    is_watched = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        exclude = ('id',)

    def get_is_collection_item(self, obj):
        profile = self.context.get("profile")
        return bool(profile.movies.filter(movie_id=obj.movie_id))

    def get_is_watched(self, obj):
        profile = self.context.get("profile")
        return bool(profile.movies_watched.filter(movie_id=obj.movie_id))

    def create(self, validated_data):
        genres_data = validated_data.pop('genres', [])
        sources_data = validated_data.pop('sources', [])
        cast_data = self.initial_data.pop('cast', [])
        crew_data = self.initial_data.pop('crew', [])

        movie = Movie.objects.create(**validated_data)

        for genre in genres_data:
            genre, created = Genre.objects.get_or_create(name=genre['name'])
            movie.genres.add(genre)

        for cast_member in cast_data:
            name = cast_member.get('name', '')
            character = cast_member.get('character', '')
            person, created = Person.objects.get_or_create(name=name)
            MovieCastMember.objects.create(movie=movie, person=person, character=character)

        for crew_member in crew_data:
            name = crew_member.get('name', '')
            job_title = crew_member.get('job_title', '')
            person, created = Person.objects.get_or_create(name=name)
            MovieCrewMember.objects.create(movie=movie, person=person, job_title=job_title)

        MovieSources.objects.create(movie=movie, **sources_data)
        return movie

    def update(self, instance, validated_data):
        profile = self.context.get("profile")

        is_collection_item = bool(profile.movies.filter(movie_id=instance.movie_id))
        is_collection_item = self.initial_data.get("is_collection_item", is_collection_item)

        if is_collection_item:
            profile.movies.add(instance)
        else:
            profile.movies.remove(instance)

        is_watched = bool(profile.movies_watched.filter(movie_id=instance.movie_id))
        is_watched = self.initial_data.get("is_watched", is_watched)

        if is_watched:
            profile.movies_watched.add(instance)
        else:
            profile.movies_watched.remove(instance)

        instance.poster = validated_data.get('poster', instance.poster)
        return instance


class MovieCollectionSerializer(serializers.ModelSerializer):
    is_watched = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('movie_id', 'poster', 'name', 'status', 'is_watched', 'release_date',)

    def get_is_watched(self, obj):
        profile = self.context.get("profile", None)
        return bool(profile.movies_watched.filter(movie_id=obj.movie_id))


class UpcomingTVShowEpisodeSerializer(serializers.ModelSerializer):
    tv_show_id = serializers.SerializerMethodField()
    tv_show = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField(method_name='get_tv_show_poster')
    type = serializers.SerializerMethodField()
    release_date = serializers.DateTimeField(source='air_date', read_only=True)

    class Meta:
        model = TVShowEpisode
        fields = ('season_number', 'episode_number', 'name', 'release_date',
                  'tv_show', 'tv_show_id', 'type', 'poster')

    def get_tv_show_id(self, obj):
        tv_show = TVShow.objects.get(seasons__episodes=obj)
        return tv_show.tv_show_id

    def get_tv_show(self, obj):
        tv_show = TVShow.objects.get(seasons__episodes=obj)
        return tv_show.name

    def get_tv_show_poster(self, obj):
        request = self.context.get("request")
        tv_show = TVShow.objects.get(seasons__episodes=obj)
        return request.build_absolute_uri(tv_show.poster.url)

    def get_type(self, obj):
        return 'TV Show'


class UpcomingMovieSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('movie_id',  'name', 'release_date', 'type', 'poster',)

    def get_type(self, obj):
        return 'Movie'


class WatchListTVShowEpisodeSerializer(serializers.ModelSerializer):
    tv_show = serializers.SerializerMethodField()

    class Meta:
        model = TVShowEpisode
        fields = ('episode_id', 'tv_show', 'season_number', 'episode_number', 'name',)

    def get_tv_show(self, obj):
        tv_show = TVShow.objects.get(seasons__episodes=obj)
        return tv_show.name


class DashboardStatisticsSerializer(serializers.ModelSerializer):
    collected_tv_shows = serializers.SerializerMethodField()
    collected_movies = serializers.SerializerMethodField()
    watched_tv_show_episodes = serializers.SerializerMethodField()
    watched_movies = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('collected_tv_shows', 'collected_movies', 'watched_tv_show_episodes', 'watched_movies',)

    def get_collected_tv_shows(self, obj):
        return obj.tv_shows.count()

    def get_collected_movies(self, obj):
        return obj.movies.count()

    def get_watched_tv_show_episodes(self, obj):
        return TVShowEpisode.objects.filter(watchers=obj).count()

    def get_watched_movies(self, obj):
        return obj.movies_watched.count()


class TVShowSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    seasons = TVShowSeasonSerializer(many=True)
    in_collection = serializers.SerializerMethodField()

    class Meta:
        model = TVShow
        exclude = ('id',)

    def get_in_collection(self, obj):
        profile = self.context.get('profile')
        return obj in profile.tv_shows.all()

    def create(self, validated_data):
        seasons_data = validated_data.pop('seasons', [])
        genres_data = validated_data.pop('genres', [])
        sources_data = validated_data.pop('sources', [])
        cast_data = validated_data.pop('cast', [])
        crew_data = validated_data.pop('crew', [])

        tv_show = TVShow.objects.create(**validated_data)

        for genre in genres_data:
            genre, created = Genre.objects.get_or_create(name=genre['name'])
            tv_show.genres.add(genre)
        tv_show.save()

        for cast_member in cast_data:
            person = Person.objects.get_or_create(name=cast_member.name)
            TVShowCastMember.objects.create(tv_show=tv_show, person=person, **cast_member)

        for crew_member in crew_data:
            person = Person.objects.get_or_create(name=crew_member.name)
            TVShowCrewMember.objects.create(tv_show=tv_show, person=person, **crew_member)

        for season in seasons_data:
            episodes_data = season.pop('episodes')
            season = TVShowSeason.objects.create(tv_show=tv_show, **season)

            for episode in episodes_data:
                TVShowEpisode.objects.create(season=season, **episode)

        if sources_data:
            TVShowSources.objects.create(tv_show=tv_show, **sources_data)

        return tv_show

    def update(self, instance, validated_data):
        instance.backdrop = validated_data.get('backdrop', instance.backdrop)
        instance.poster = validated_data.get('poster', instance.poster)
        return instance
