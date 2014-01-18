from django.conf.urls import patterns, url


urlpatterns = patterns('userlogin.views',
                       url(r'^$', 'home', name='home'),
                       url(r'^login$', 'login_handler', name='login_handler'),
                       url(r'^logout$', 'logout_handler', name='logout_handler'),
                       url(r'^users$', 'users', name='show_users'),
                       url(r'^users/add$', 'add_user', name='add_user'),
                       url(r'^users/upload_list$', 'upload_user_list', name='upload_user_list'),
                       url(r'^user/set_branch$', 'set_branch', name='set_branch'),
                       url(r'^user/get_message$', 'get_message', name='get_message'),
)
