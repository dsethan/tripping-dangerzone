from django.conf.urls import patterns, url
from drivers import views

urlpatterns = patterns('',
    url(r'^$', views.driver_dash, name='driver_dash'),


    )