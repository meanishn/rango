from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'tango_with_django.views.home', name='home'),
    url(r'^rango/', include('rango.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('user_sessions.urls', 'user_sessions')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}),
        
    )