from django.conf.urls import patterns, url
from dashboard import views

urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^order_management/$', views.order_management, name='order_management'),
    url(r'^populate_menu', views.populate_menu, name='populate_menu'),
    url(r'^depopulate_menu', views.depopulate_menu, name='depopulate_menu'),
    url(r'^remove_all_dispatches', views.remove_all_dispatches, name='remove_all_dispatches'),
    url(r'^drivers/assign_times/process_driver_add', views.process_driver_add, name='process_driver_add'),
    url(r'^drivers/assign_times', views.assign_times, name='assign_times'),
    url(r'^drivers/add_driver', views.add_driver, name='add_driver'),
    url(r'^drivers', views.drivers, name='drivers'),
    url(r'^financials', views.financials, name='financials'),
    url(r'^data', views.data, name='data'),

    )