
# URLs der Planung

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

api_router = DefaultRouter()
api_router.register(r'ak', views.AKViewSet)
api_router.register(r'room', views.RoomViewSet)
api_router.register(r'slot', views.RoomAvailabilityViewSet)
api_router.register(r'aktermin', views.AKTerminViewSet)

urlpatterns = [
    url(r'^$', views.oplan_home, name="oplan_home"),
    url(r'^api/', include(api_router.urls)),
    url(r'akwall/$', views.ak_wall, name="ak_wall"),
    url(r'check_constraints/$', views.check_all_constraints, name="check_constraints"),
    url(r'akwall/beamer/$', views.ak_wall_beamer, name="ak_wall_beamer"),
    url(r'ak/(?P<akid>[0-9]+)/$', views.ak_details, name="ak_details"),
    url(r'infoscreen/$', views.infoscreen, name="infoscreen"),
    url(r'infoscreen/beamer/$', views.infoscreen_beamer, name="infoscreen_beamer"),
    url(r'darwin_status/$', views.darwin_status, name="darwin_status"),
    url(r'roomcalendar/$', views.roomlist, name="roomlist"),
    url(r'roomcalendar/(?P<roomnumber>[^/]+)/$', views.roomcalendar, name="roomcalendar"),
    url(r'roomcalendar/(?P<roomnumber>[^/]+)/$', views.roomcalendar, name="roomcalendar"),
    url(r'import/rooms/csv/$', views.ImportRaumliste.as_view(), name="import_room_list"),
    url(r'import/rooms/dekrr/$', views.ImportDekrr.as_view(), name="import_room_dekrr"),
    
    url(r'import/aks-wiki/$', views.ImportWikiAkListe.as_view(), name="import_aks_wikitext"),
    url(r'roomevents/$', views.RoomAvailabilityApi.as_view(), name="room_get_slots"),
    
    
    
    #url(r'signs/$', views.Schildergenerator.as_view()),
]
