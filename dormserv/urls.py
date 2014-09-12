from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dormserv.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('users.urls')),
    url(r'^cal/', include('cal.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^menu/', include('menu.urls')),
    url(r'^checkout/', include('checkout.urls')),
    url(r'^drivers/', include('drivers.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^kitchen/', include('kitchen.urls')),
    #url(r'^process/', include('process.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
)

if not settings.DEBUG:
   urlpatterns += patterns('',
       (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
   )