from django.conf.urls.defaults import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^server/', include('server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'mobile.views.index'),
    (r'^register/user$', 'mobile.views.register_user'),
    (r'^register/gps$', 'mobile.gps_log.main'),
    
    (r'^delete/log$', 'mobile.views.delete_log'),
    (r'^delete/user$', 'mobile.views.delete_user'),
    
    (r'^follow$', 'mobile.views.follow'),
    (r'^unfollow$', 'mobile.views.unfollow'),
    
    
    (r'^gps/direction$', 'mobile.gps.getDirections'),
    
    
    (r'^test$', 'mobile.views.test'),
    (r'^direction$', 'mobile.views.direction_test'),
    
    (r'^admin/', include(admin.site.urls)),
)
