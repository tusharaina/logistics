from django.conf.urls import patterns, url
from transit.urls import urlpatterns as transit_urls

urlpatterns = patterns('awb.views',
                       #url(r'home$',TemplateView.as_view(template_name='client/pincode.html'), name="home"),
                       url(r'^awb/incoming$', 'awb_incoming', name='awb_incoming'),
                       url(r'^awb/outgoing$', 'awb_outgoing', name='awb_outgoing'),
                       url(r'^awb/print_invoice$', 'awb_print_invoice', name='awb_print_invoice'),
                       url(r'^awb/mis$', 'awb_generate_mis', name='awb_generate_mis'),
                       url(r'^awb/mis/download$', 'awb_download_mis', name='awb_download_mis'),
                       url(r'^awb/report/cc', 'awb_report_cc', name='awb_report_cc'),
                       url(r'^awb/field_update$', 'awb_field_update', name='awb_field_update'),
                       url(r'^awb/(\d+)$', 'awb_history', name='awb_history'),
                       url(r'^awb/status_update$', 'awb_status_update', name='status_update$'),
                       url(r'^manifest/report$', 'manifest', name='show_manifest'),
                       url(r'^manifest/upload$', 'upload_manifest_file', name='upload_manifest_file'),
                       url(r'^manifest/in_scanning$', 'awb_in_scanning', name='awb_in_scanning'),
                       url(r'^awb/in_scanning$', 'awb_in_scanning', name='awb_in_scanning'),
                       url(r'^manifest/(\d+)$', 'manifest_detail', name='manifest_detail'),
                       #url(r'^manifest/(\d+)/invoice$', 'manifest_invoice', name='manifest_invoice'),
                       url(r'^awb/print_invoice_sheet$', 'awb_print_invoice_sheet', name='print_invoice_sheet'),
                       url(r'^search/(?P<extra>.*)$', 'search_awb', name='search_awb'),
)

urlpatterns += transit_urls
