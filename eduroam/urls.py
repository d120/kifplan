from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^import/', views.ImportGuestAccounts.as_view(), name='import_guest_acc'),
]
