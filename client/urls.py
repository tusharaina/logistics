from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('client.views',
                       #url(r'home$',TemplateView.as_view(template_name='client/pincode.html'), name="home"),
                       url(r'^$', 'client', name='show_client'),
                       url(r'^add$', 'add_client', name='add_client'),
                       url(r'^get_warehouses$', 'get_client_warehouses', name='get_client_warehouses'),
                       url(r'^warehouse$', 'client_warehouse', name='show_client_warehouse'),
                       url(r'^warehouse/add$', 'add_client_warehouse', name='add_client_warehouse'),
)
