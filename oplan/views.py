from django.shortcuts import render
from django.views.generic import View
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied

from rest_framework import viewsets, permissions, filters

from oplan.models import AK, Room, RoomOpening

from oplan.serializers import AKSerializer, RoomSerializer, RoomOpeningSerializer
import csv

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


class ImportRaumliste(View):
    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.create_room'): raise PermissionDenied
        foo = ""
        return render(request, "oplan/ak_import_view.html", { 'titel': 'Raumliste importieren (Format: "Raumnummer,Kapazität")', 'output': '' })
    
    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.create_room'): raise PermissionDenied
        
        the_csv = request.POST["content"]
        reader = csv.reader(the_csv.splitlines())
        
        out=""
        for line in reader:
            out += '<li>Raum "' + line[0] + '" ...'
            try:
                Room.objects.create(number=line[0],
                    type='SR', capacity=line[1])
                out += "ok"
            except IntegrityError as ex:
                out += str(ex)
            
        
        
        
        return render(request, "oplan/ak_import_view.html", { 'titel': 'Raumliste importieren', 'output': out })



