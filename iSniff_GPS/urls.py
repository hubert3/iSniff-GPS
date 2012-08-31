from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ClientList.as_view()),
    url(r'^client/(?P<slug>[:\w]+)$', ClientDetail.as_view()),
    url(r'^clients/?$', ClientList.as_view()),
    url(r'^network/(?P<ssid_or_bssid>.+)$', APDetail.as_view()),
    url(r'^networks/?$', APList.as_view()),
    url(r'^apple-wloc/?$', AppleWloc),
    url(r'^apple-wloc/(?P<bssid>[:\w]+)$', AppleWloc),
    url(r'^updateSSID$', updateSSID),
    url(r'^locateSSID/?$', locateSSID),
    url(r'^locateSSID/(?P<ssid>[\w\W]+)$', locateSSID),
    url(r'^stats/?$', stats.as_view()),

    url(r'^admin/', include(admin.site.urls)),)

