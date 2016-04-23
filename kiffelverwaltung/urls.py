from django.conf.urls import include, url
from django.contrib import admin, auth
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^', include('frontend.urls', namespace='frontend', app_name='frontend')),
    url(r'^api/v1/eduroam/', include('eduroam.urls', namespace='eduroam', app_name='eduroam')),
    url(r'^plan/', include('oplan.urls', namespace='oplan', app_name='oplan')),
    url(r'^api/v1/', include('kiffel.urls', namespace='kiffel', app_name='kiffel')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    
    
    url(r'^login/$', auth.views.login, {'template_name': 'oplan/login.html'},
        name='mysite_login'),
    url(r'^logout/$', auth.views.logout,
        {'next_page': reverse_lazy('oplan:oplan_home')}, name='mysite_logout'),
    
    
]
