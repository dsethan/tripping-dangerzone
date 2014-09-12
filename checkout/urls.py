from django.conf.urls import patterns, url
from checkout import views

urlpatterns = patterns('',
    #url(r'^$', views.checkout, name='checkout'),
    url(r'^process_order', views.process_order, name='process_order'),
    url(r'^process', views.process, name='process'),

	#url(r'^payment', views.charge, name='charge'),


    )
