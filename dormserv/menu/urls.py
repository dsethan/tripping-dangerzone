from django.conf.urls import patterns, url
from menu import views

urlpatterns = patterns('',
    url(r'^$', views.display_menu, name='display_menu'),
	url(r'^add_item', views.add_item, name='add_item'),

    )
