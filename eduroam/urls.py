from django.conf.urls import url, include

from . import views

app_name='eduroam'

urlpatterns = [
    url(r'^import/', views.ImportGuestAccounts.as_view(), name='import_guest_acc'),
    url(r'^assign/', views.AssignGuestAccount.as_view(), name='assign_guest_acc'),
]
