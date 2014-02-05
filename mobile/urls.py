from django.conf.urls import patterns, url

urlpatterns = patterns('mobile.views',
                       #url(r'home$',TemplateView.as_view(template_name='client/pincode.html'), name="home"),
                       url(r'^aw$', 'aw', name='aw'),
                       url(r'^awb_history_mobile', 'awb_history_mobile', name='awb_history_mobile'),
)