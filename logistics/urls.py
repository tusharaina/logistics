from django.conf.urls import patterns, include, url
from django.contrib import admin
from settings import STATIC_ROOT
from transit.views import reports

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),
                       url('^admin/', include(admin.site.urls)),
                       url(r'^client/', include('client.urls')),
                       url(r'^internal/', include('internal.urls')),
                       url(r'^zoning/', include('zoning.urls')),
                       url(r'^transit/', include('awb.urls')),
                       url(r'^reports/(?P<type>generic|cash-report)$', reports),
                       url(r'^', include('userlogin.urls')),
)
