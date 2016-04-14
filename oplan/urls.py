
# URLs der Planung

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'ak', views.AKViewSet)
router.register(r'room', views.RoomViewSet)
router.register(r'slot', views.RoomOpeningViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'raumimport/$', views.ImportRaumliste.as_view(), name="import_room_list"),
    url(r'import/aks-wiki/$', views.ImportWikiAkListe.as_view(), name="import_aks_wikitext"),
    #url(r'signs/$', views.Schildergenerator.as_view()),
]
