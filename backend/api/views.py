import difflib
from datetime import datetime, timezone, timedelta
from dateutil.tz import tzutc
from django.utils import timezone
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import authentication
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from api.permission import UserCustomPermission
from api.utilities.emails import send_reset_password_email, send_account_verification_email, send_feedback_email, \
    send_recommendation_email
from api.models import UserProfile, TVShow, TVShowEpisode, Movie
from api.serializers import UserProfileSerializer, TVShowSerializer, TVShowSearchSerializer, TVShowDetailsSerializer, \
    TVShowEpisodeSerializer, TVShowCollectionSerializer, MovieDetailsSerializer, MovieSearchSerializer, \
    MovieCollectionSerializer, UpcomingTVShowEpisodeSerializer, UpcomingMovieSerializer, \
    WatchListTVShowEpisodeSerializer, DashboardStatisticsSerializer


class UsersView(APIView):
    """
    A view for the users and admins.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (UserCustomPermission,)

    @staticmethod
    def post(request):
        """
        Create new user and user profile.
        """
        serializer = UserProfileSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            send_account_verification_email(serializer.data['email_address'])
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request):
        """
        Update user and the user profile.
        """
        profile = get_object_or_404(UserProfile, user=request.user)

        if request.data.get('password'):
            if request.data.get('old_password'):
                is_valid = request.user.check_password(request.data.get('old_password'))
                if not is_valid:
                    content = {
                        'old_password': 'The old password is incorrect.'
                    }
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        """
        Get user profile.
        """
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(profile, context={'profile': profile, 'request': request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class AccountRecoveryView(APIView):
    """
    A view for recovering an users' password.
    """

    @staticmethod
    def post(request):
        """
        Request a password reset email with reset token.
        """
        send_reset_password_email(request.data.get('email_address'))
        content = {'status': 'E-mail has been sent.'}
        return Response(content, status=status.HTTP_200_OK)

    @staticmethod
    def put(request):
        """
        Change password.
        """
        token = request.data.get('token')
        password = request.data.get('password')

        try:
            profile = UserProfile.objects.get(password_recovery_token=token)

            if abs(timezone.now() - profile.password_recovery_at).seconds < 1800:
                profile.password_recovery_at = None
                profile.password_recovery_token = None
                profile.save()

                user = profile.user
                user.set_password(password)
                user.save()
                content = {'status': 'Password has been changed.'}
                return Response(content, status=status.HTTP_200_OK)
            else:
                content = {'status': 'The token is invalid.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        except UserProfile.DoesNotExist:
            content = {'status': 'The token is invalid.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class AuthenticationView(APIView):
    """
    A view for authorizing users.
    """

    @staticmethod
    def get(request):
        send_account_verification_email(request.user.email)
        content = {'status': 'Verification e-mail has been sent.'}
        return Response(content, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        """
        Verify username and password.
        """
        email_address = request.data.get('email_address')
        password = request.data.get('password')
        user = authenticate(username=email_address, password=password)

        if user is not None:
            user_profile = get_object_or_404(UserProfile, user=user)

            # Renew Token
            try:
                Token.objects.get(user=user).delete()
            except Token.DoesNotExist:
                pass

            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        content = {'status': 'Unauthorized'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def put(request):
        """
        Verify the users' account.
        """
        profile_id = request.data.get('profile_id')

        try:
            profile = UserProfile.objects.get(profile_id=profile_id)
            profile.is_verified = True
            profile.save()
            content = {'status': 'Account is verified.'}
            return Response(content, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            content = {'status': 'The token is invalid.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class UserTVShowCollectionView(APIView):
    """
    A view for the tv-shows collection of current user.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def get(request):
        """
        Retrieve tv-shows collection of the current user.
        """
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = TVShowCollectionSerializer(profile.tv_shows, many=True,
                                                context={'profile': profile, 'request': request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class UserMovieCollectionView(APIView):
    """
    A view for the movies collection of current user.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def get(request):
        """
        Retrieve movies collection of the current user.
        """
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = MovieCollectionSerializer(profile.movies, many=True,
                                               context={'profile': profile, 'request': request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class DashboardUpcomingReleasesView(APIView):
    """
    A view for TV Show and Movies upcoming releases.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def get(request):
        """
        Retrieve upcoming releases.
        """
        profile = get_object_or_404(UserProfile, user=request.user)
        request_date = request.query_params.get('date', None)

        if request_date:
            start_date = datetime.fromtimestamp(float(request_date)/1000, tzutc())
        else:
            start_date = timezone.now()

        upcoming_episodes = TVShowEpisode.objects.filter(season__tv_show__collectors=profile,
                                                         air_date__range=(start_date, start_date + timedelta(days=7)))
        upcoming_movies = Movie.objects.filter(collectors=profile,
                                               release_date__range=(start_date, start_date + timedelta(days=7)))

        episodes_serializer = UpcomingTVShowEpisodeSerializer(upcoming_episodes, many=True,
                                                              context={'request': request})
        movies_serializer = UpcomingMovieSerializer(upcoming_movies, many=True, context={'request': request})
        upcoming_media = sorted(episodes_serializer.data + movies_serializer.data, key=lambda x: x['release_date'])
        return Response(upcoming_media, status=status.HTTP_200_OK)


class DashboardWatchListView(APIView):
    """
    A view for TV Show watch list.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def get(request):
        """
        Retrieve watch list.
        """
        profile = get_object_or_404(UserProfile, user=request.user)
        request_date = request.query_params.get('date', None)

        if request_date:
            start_date = datetime.fromtimestamp(float(request_date)/1000)
        else:
            start_date = timezone.now()

        watch_list = []
        for tv_show in profile.tv_shows.all():
            episode = TVShowEpisode.objects.filter(season__tv_show=tv_show,
                                                   air_date__lte=start_date).exclude(watchers=profile).first()
            if episode:
                watch_list.append(episode)

        serializer = WatchListTVShowEpisodeSerializer(watch_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DashboardStatisticsView(APIView):
    """
    A view for Dashboard statistics.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def get(request):
        """
        Retrieve statistics.
        """
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = DashboardStatisticsSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedbackView(APIView):
    """
    A view for Feedback.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def post(request):
        """
        Send feedback to admin.
        """
        send_feedback_email(request.user, request.data.get('message'), request.data.get('feedback_type'))
        content = {'status': 'Feedback has been sent.'}
        return Response(content, status=status.HTTP_200_OK)


class RecommendationView(APIView):
    """
    A view for Recommendation.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def post(request):
        """
        Send Recommendation to somebody.
        """
        media_type = request.data.get('media_type')
        if media_type == 'TV Show':
            media = get_object_or_404(TVShow, tv_show_id=request.data.get('tv_show_id'))
        else:
            media = get_object_or_404(Movie, movie_id=request.data.get('movie_id'))

        send_recommendation_email(request.user, request.data.get('recipient'), media_type, media)
        content = {'status': '%s Recommendation has been sent.' % media_type}
        return Response(content, status=status.HTTP_200_OK)


class TVShowView(APIView):
    """
    A view for TV Shows.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def post(request):
        """
        Create new TV Show.
        """
        serializer = TVShowSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TVShowDetailsView(APIView):
    """
    A view for TV Show Details.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def get(request, tv_show_id):
        """
        Get TV Show Details.
        """
        profile = get_object_or_404(UserProfile, user=request.user)
        tv_show = get_object_or_404(TVShow, tv_show_id=tv_show_id)
        serializer = TVShowDetailsSerializer(tv_show, context={'profile': profile, 'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, tv_show_id):
        """
        Update TV Show Details
        """
        tv_show = get_object_or_404(TVShow, tv_show_id=tv_show_id)
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = TVShowDetailsSerializer(tv_show, data=request.data, partial=True, context={'profile': profile,
                                                                                                'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TVShowImagesView(APIView):
    """
    A view for TV Shows.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    parser_classes = (MultiPartParser,)

    @staticmethod
    def post(request, tv_show_id):
        """
        Create new TV Show.
        """
        tv_show = TVShow.objects.get(tv_show_id=tv_show_id)
        serializer = TVShowSerializer(tv_show, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TVShowEpisodesDetailsView(APIView):
    """
    A view for TV Show Episode Details.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def put(request, episode_id):
        """
        Update TV Show Episode Details
        """
        episode = get_object_or_404(TVShowEpisode, episode_id=episode_id)
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = TVShowEpisodeSerializer(episode, data=request.data, partial=True, context={'profile': profile,
                                                                                                'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailsView(APIView):
    """
    A view for the details of a Movie.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def get(request, movie_id):
        """
        Retrieve details of a Movie.
        """
        profile = get_object_or_404(UserProfile, user=request.user)
        movie = get_object_or_404(Movie, movie_id=movie_id)
        serializer = MovieDetailsSerializer(movie, context={'request': request, 'profile': profile})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @staticmethod
    def put(request, movie_id):
        """
        Update Movie details
        """
        movie = get_object_or_404(Movie, movie_id=movie_id)
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = MovieDetailsSerializer(movie, data=request.data, partial=True, context={'profile': profile,
                                                                                             'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def post(request):
        """
        Create new Movie.
        """
        serializer = MovieDetailsSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieImagesView(APIView):
    """
    A view for the images of a movie.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    parser_classes = (MultiPartParser,)

    @staticmethod
    def post(request, movie_id):
        """
        Add image to a movie
        """
        movie = get_object_or_404(Movie, movie_id=movie_id)
        serializer = MovieDetailsSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchView(APIView):
    """
    A view for searching TV Shows and Movies.
    """
    authentication_classes = (authentication.TokenAuthentication,)

    @staticmethod
    def get(request):
        """
        Search for a TV Show or Movie
        """

        query = request.query_params.get('query', None)
        tv_shows = movies = []
        if query and len(query) > 3:
            tv_shows = TVShow.objects.filter(name__icontains=query.lower())

            for tv_show in tv_shows:
                tv_show.order = difflib.SequenceMatcher(None, tv_show.name, query).ratio()

            movies = Movie.objects.filter(name__icontains=query)
            for movie in movies:
                movie.order = difflib.SequenceMatcher(None, movie.name, query).ratio()

        tv_shows_serializer = TVShowSearchSerializer(tv_shows, many=True)
        movies_serializer = MovieSearchSerializer(movies, many=True)
        media = sorted(tv_shows_serializer.data + movies_serializer.data, key=lambda x: x['order'], reverse=True)[:20]
        return Response(media, status=status.HTTP_200_OK)
