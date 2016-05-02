
# URLs der Kiffel-App

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'kiffels', views.KiffelViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'reports/$', views.KiffelAttendingReport.as_view()),
    url(r'nametags/$', views.NametagsExport.as_view()),
    url(r'signs/$', views.Schildergenerator.as_view()),
    url(r'import/engelsystem/$', views.ImportFromEngelsystem.as_view(), name='import_personen_engel'),
    url(r'import/anmeldung/$', views.ImportFromKiffelAnmeldung.as_view(), name='import_personen'),
    url(r'createanonym/$', views.CreateAnonymPerson.as_view(), name='createanonym'),
    url(r'export/bmbf/$', views.ExportBMBF.as_view(), name='export_bmbf'),
    url(r'mobi/$', views.anmeldung_mobile, name='mobi'),
    
]
