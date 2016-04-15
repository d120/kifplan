
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
    url(r'akwall/$', views.ak_wall, name="ak_wall"),
    url(r'infoscreen/$', views.infoscreen, name="infoscreen"),
    url(r'darwin_status/$', views.darwin_status, name="darwin_status"),
    url(r'raum/(?P<raumnummer>\w+)/$', views.raumansicht, name="raumansicht"),
    url(r'raum/(?P<raumnummer>\w+)/$', views.raumansicht, name="raumansicht"),
    url(r'raumimport/$', views.ImportRaumliste.as_view(), name="import_room_list"),
    url(r'import/aks-wiki/$', views.ImportWikiAkListe.as_view(), name="import_aks_wikitext"),
    #url(r'signs/$', views.Schildergenerator.as_view()),
]
