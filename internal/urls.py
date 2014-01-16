from django.conf.urls import patterns, url

urlpatterns = patterns('internal.views',
                       #url(r'home$',TemplateView.as_view(template_name='client/pincode.html'), name="home"),
                       url(r'^branch$', 'branch', name='show_branch'),
                       url(r'^branch/add$', 'add_branch', name='add_branch'),
                       url(r'^branch_pincode/add$', 'add_branch_pincode', name='add_branch_pincode'),
                       url(r'^employee$', 'employee', name='show_employee'),
                       url(r'^employee/add$', 'add_employee', name='add_employee'),
                       url(r'^vehicle$', 'vehicle', name='show_vehicle'),
                       url(r'^vehicle/add$', 'add_vehicle', name='add_vehicle'),
                       url(r'^vehicle/upload_list$', 'upload_vehicle_list', name='vehicle_upload_list'),
                       url(r'^branch/upload$', 'upload_branch_pincode', name='upload_branch_pincode'),
                       url(r'^branch/(\d+)/pincode$', 'branch_pincode', name='show_branch_pincode'),
                       url(r'^branch/get_all$', 'branch_get_all', name='branch_get_all'),
)
