from django.conf.urls import patterns, url
from cal import views

urlpatterns = patterns('',
    url(r'^$', views.display_calendar, name='display_calendar'),
    url(r'^(?P<entry_id>\d+)/$', views.menu_reroute, name='menu_reroute'),
    )
