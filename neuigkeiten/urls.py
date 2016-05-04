
# URLs der Neuigkeiten-App

from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    url(r'^$', views.list_all, name='list_all'),
    url(r'^rss$', views.list_rss, name='list_rss'),
    
    url(r'api/push/$', views.PushNotification.as_view()),
    url(r'api/notifications/$', csrf_exempt(views.PushRetrieveNotification.as_view())),
]
