from django.conf.urls import patterns, url
from drivers import views

urlpatterns = patterns('',
    url(r'^$', views.driver_login, name='driver_login'),
	url(r'^driver_dash', views.driver_dash, name='driver_dash'),


    )