
# URLs der Kiffel-App

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required


from . import views

router = DefaultRouter()
router.register(r'kiffels', views.KiffelViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'reports/$', views.KiffelAttendingReport.as_view()),
    url(r'nametags/$', views.NametagsExport.as_view()),
    url(r'signs/$', views.Schildergenerator.as_view()),
    url(r'import/engelsystem/$', login_required(views.ImportFromEngelsystem.as_view()), name='import_personen_engel'),
    url(r'import/anmeldung/$', login_required(views.ImportFromKiffelAnmeldung.as_view()), name='import_personen'),
    url(r'createanonym/$', login_required(views.CreateAnonymPerson.as_view()), name='createanonym'),
    url(r'export/bmbf/$', login_required(views.ExportBMBF.as_view()), name='export_bmbf'),
    url(r'mobi/$', login_required(views.anmeldung_mobile), name='mobi'),
    
]
