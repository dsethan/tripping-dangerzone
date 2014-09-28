from django.conf.urls import patterns, url
from kitchen import views

urlpatterns = patterns('',
	url(r'^$', views.kitchen_login, name='kitchen_login'),
    url(r'^kitchen_dash', views.kitchen, name='kitchen'),
    )