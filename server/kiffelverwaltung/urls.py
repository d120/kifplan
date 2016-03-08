from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('kiffel.urls', namespace='kiffel', app_name='kiffel')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
]
