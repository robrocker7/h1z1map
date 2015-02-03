from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('server.apis.urls', namespace='api')),
    url(r'^$', 'server.common.views.index', name='index'),
)
