from django.conf.urls import patterns, url
from kitchen import views

urlpatterns = patterns('',
    url(r'^$', views.kitchen, name='kitchen'),
    )