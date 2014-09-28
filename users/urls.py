from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
	url(r'^$', views.user_login, name='login'),
    url(r'^register', views.register, name='register'), # ADD NEW PATTERN!
	url(r'^login/$', views.user_login, name='login'), # ADD NEW PATTERN!
	url(r'^logout/$', views.user_logout, name='logout'), # ADD NEW PATTERN!
	url(r'^register/thanks/$', views.thanks, name='thanks'), # ADD NEW PATTERN!
	url(r'^register/welcome/$', views.thanks, name='thanks'), # ADD NEW PATTERN!
	url(r'^faq', views.faq, name='faq'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^privacy', views.privacy, name='privacy'),
    )
