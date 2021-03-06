from django.conf.urls import patterns, url
from mytube import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^add_movie/$', views.add_movie, name='add_movie'),
                       url(r'^genre/(?P<genre_name_url>\w+)/$', views.genre, name='genre'),
                       url(r'^movie/(?P<movie_id>\d+)/$', views.movie, name='movie'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^profile/$', views.profile, name='profile'),
                       url(r'^goto/$', views.track_url, name='track_url'),
                       url(r'^like_genre/$', views.like_genre, name='like_genre'),
                       url(r'^search_movie/$', views.search_movie, name='search_movie'),
                       )

