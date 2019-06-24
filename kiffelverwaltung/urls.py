from django.conf.urls import include, url
from django.contrib import admin, auth
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from ajax_select import urls as ajax_select_urls
from django.contrib.auth import views as auth_views
from oplan import views as ov

urlpatterns = [
    url(r'^$', ov.oplan_home, name="oplan_home"),

    url(r'^', include('frontend.urls', namespace='frontend', app_name='frontend')),
    url(r'^api/v1/eduroam/', include('eduroam.urls', namespace='eduroam', app_name='eduroam')),
    url(r'^plan/', include('oplan.urls', namespace='oplan', app_name='oplan')),
    url(r'^kiffel/', include('kiffel.urls', namespace='kiffel', app_name='kiffel')),
    url(r'^news/', include('neuigkeiten.urls', namespace='neuigkeiten', app_name='neuigkeiten')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^service_worker.js$',
        TemplateView.as_view(template_name='oplan/service_worker.js', 
            content_type='application/x-javascript')),
    
    url(r'^login/$', auth.views.login, {'template_name': 'oplan/login.html'},
        name='mysite_login'),
    url(r'^logout/$', auth.views.logout,
        {'next_page': reverse_lazy('frontend:index')}, name='mysite_logout'),
    
    
    url(r'^user/password/reset/$', 
        auth_views.password_reset, 
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        auth_views.password_reset_done),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
        auth_views.password_reset_confirm, 
        {'post_reset_redirect' : '/user/password/done/'},
        name="django.contrib.auth.views.password_reset_confirm"),
    url(r'^user/password/done/$', 
        auth_views.password_reset_complete),
    
    # place it at whatever base url you like
    url(r'^ajax_select/', include(ajax_select_urls)),
]
