from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'guest-accounts', views.GuestAccountViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
