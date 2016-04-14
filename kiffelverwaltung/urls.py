from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('frontend.urls', namespace='frontend', app_name='frontend')),
    url(r'^api/v1/eduroam/', include('eduroam.urls', namespace='eduroam', app_name='eduroam')),
    url(r'^api/v1/oplan/', include('aks.urls', namespace='aks', app_name='aks')),
    url(r'^api/v1/', include('kiffel.urls', namespace='kiffel', app_name='kiffel')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]
