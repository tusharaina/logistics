from django.conf.urls import patterns, include, url
from django.contrib import admin
from transit.views import reports
from settings import STATIC_ROOT, MEDIA_ROOT

urlpatterns = patterns('',
                       # Examples:
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('userconfig.urls'))

)