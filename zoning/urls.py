from django.conf.urls import patterns, url

urlpatterns = patterns('zoning.views',
                       url(r'^zone$', 'zone', name='show_zone'),
                       url(r'^zone/add$', 'add_zone', name='add_zone'),
                       url(r'^city$', 'city', name='show_city'),
                       url(r'^city/add$', 'add_city', name='add_city'),
                       url(r'^pincode$', 'pincode', name='show_pincode'),
                       url(r'^pincode/search$', 'pincode_search', name='pincode_search'),
                       url(r'^pincode/add$', 'add_pincode', name='add_pincode'),
                       url(r'^upload$', 'upload_file', name='upload_file'),
)
