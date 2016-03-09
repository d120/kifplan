from rest_framework import viewsets, permissions

from kiffel.models import Kiffel
from kiffel.serializers import KiffelSerializer

class KiffelViewSet(viewsets.ModelViewSet):
    serializer_class = KiffelSerializer
    queryset = Kiffel.objects.all()
