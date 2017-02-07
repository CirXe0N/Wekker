from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.UsersView.as_view()),
    url(r'^account/authentication/$', views.AuthenticationView.as_view()),
    url(r'^account/recovery/$', views.AccountRecoveryView.as_view()),
    url(r'^collections/tv-shows/$', views.UserTVShowCollectionView.as_view()),
    url(r'^collections/movies/$', views.UserMovieCollectionView.as_view()),
    url(r'^dashboard/upcoming-releases/$', views.DashboardUpcomingReleasesView.as_view()),
    url(r'^dashboard/watch-list/$', views.DashboardWatchListView.as_view()),
    url(r'^dashboard/statistics/$', views.DashboardStatisticsView.as_view()),
    url(r'^tv-shows/$', views.TVShowView.as_view()),
    url(r'^tv-shows/(?P<tv_show_id>[a-zA-Z0-9-]+)/$', views.TVShowDetailsView.as_view()),
    url(r'^tv-show-episodes/(?P<episode_id>[a-zA-Z0-9-]+)/$', views.TVShowEpisodesDetailsView.as_view()),
    url(r'^tv-shows/(?P<tv_show_id>[a-zA-Z0-9-]+)/images/$', views.TVShowImagesView.as_view()),
    url(r'^movies/$', views.MovieDetailsView.as_view()),
    url(r'^movies/(?P<movie_id>[a-zA-Z0-9-]+)/$', views.MovieDetailsView.as_view()),
    url(r'^movies/(?P<movie_id>[a-zA-Z0-9-]+)/images/$', views.MovieImagesView.as_view()),
    url(r'^search/$', views.SearchView.as_view()),
    url(r'^feedback/$', views.FeedbackView.as_view()),
    url(r'^recommendation/$', views.RecommendationView.as_view()),
]
