from django.shortcuts import render

from rest_framework import viewsets, permissions, filters

from aks.models import AK, Room, RoomOpening

from aks.serializers import AKSerializer, RoomSerializer, RoomOpeningSerializer

# Views für die Planungsapp

class AKViewSet(viewsets.ModelViewSet):
    serializer_class = AKSerializer
    queryset = AK.objects.all()
    filter_fields = [f.name for f in AK._meta.get_fields()]
    search_fields = [f.name for f in AK._meta.get_fields()]
    ordering_fields = [f.name for f in AK._meta.get_fields()]


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    filter_fields = [f.name for f in Room._meta.get_fields()]
    search_fields = [f.name for f in Room._meta.get_fields()]
    ordering_fields = [f.name for f in Room._meta.get_fields()]


class RoomOpeningViewSet(viewsets.ModelViewSet):
    serializer_class = RoomOpeningSerializer
    queryset = RoomOpening.objects.all()
    filter_fields = [f.name for f in RoomOpening._meta.get_fields()]
    search_fields = [f.name for f in RoomOpening._meta.get_fields()]
    ordering_fields = [f.name for f in RoomOpening._meta.get_fields()]



