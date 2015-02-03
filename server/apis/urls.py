from django.conf.urls import patterns, include, url


urlpatterns = patterns('server.apis.player_api',
    url(r'^player/all/$', 'get_all_players', name='get_all_players'),
    url(r'^player/add/$', 'add_or_login_player', name='add_or_login_player'),
    url(r'^player/update/$', 'update_player', name='update_player'),
    url(r'^player/$', 'get_player', name='get_player'),
)