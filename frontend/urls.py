from django.conf.urls import url, include

from . import views

app_name='frontend'

urlpatterns = [
    url(r'^index/$', views.Index.as_view(), name="index"),
    url(r'^beamer/$', views.beamer_multi),
]
