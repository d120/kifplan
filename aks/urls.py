
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
    #url(r'reports/$', views.KiffelAttendingReport.as_view()),
    #url(r'nametags/$', views.NametagsExport.as_view()),
    #url(r'signs/$', views.Schildergenerator.as_view()),
]
