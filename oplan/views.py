from django.shortcuts import render
from django.views.generic import View
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse


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


def roomcalendar(request, roomnumber, *args, **kwargs):
    room = Room.objects.get(number=roomnumber)
    return render(request, "oplan/roomcalendar.html", { 'titel': 'Rauminfo '+room.number, 'room': room })

class RoomSlotsApi(View):
    def get(self, request, *args, **kwargs):
        para = request.GET
        objs = RoomOpening.objects.filter(room__id=para['room'], start_time__range=[ para['start'], para['end'] ])
        qq = []
        for obj in objs:
            qq.append({ 'id': obj.id, 'start': obj.start_time, 'end': obj.start_time + obj.duration, 'title': obj.room.number })
        return JsonResponse({ 'slots' : qq })
        
    def post(self, request, *args, **kwargs):
        return JsonResponse({ 'success': '???' })
    

# TODO

def ak_wall(request, *args, **kwargs):
    return render(request, "oplan/ak_import_view.html", { 'titel': 'TODO: AK-Wall ', 'out': '' })

def infoscreen(request, *args, **kwargs):
    return render(request, "oplan/ak_import_view.html", { 'titel': 'TODO: Infoscreen ', 'out': '' })

def darwin_status(request, *args, **kwargs):
    return render(request, "oplan/ak_import_view.html", { 'titel': 'TODO: Automatische AK-Zuordnung ("Darwin") - Status ', 'out': '' })

import re

class ImportWikiAkListe(View):
    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.create_room'): raise PermissionDenied
        foo = ""
        return render(request, "oplan/ak_import_view.html", { 'titel': 'AKs importieren (Quelltext der Wikiseite hier pasten)', 'output': '' })
    
    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.create_room'): raise PermissionDenied
        
        wikitext = request.POST["content"]
        
        rx = re.compile(r"""
        ^\s*\{\{Ak\sSpalte[\sa-z0-9]*
        (.*?)
        ^\s*\}\}
        """, re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE)
        rx2 = re.compile(r"""
        ^\|\s*([a-z]+)\s*=(.*?)$
        """, re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE)
        rx_link = re.compile(r"\s+")
        
        out="Ergebnis:"
        out+="<table>"
        
        for ak_match in rx.finditer(wikitext):
            out += "<tr>"
            ak_str = ak_match.group(1)
            data = {'wer': 'N.N.', 'wann': '?', 'wieviele': '?', 'dauer': '?', 'beschreibung': '', 'name': '', 'link': ''}
            for line_match in rx2.finditer(ak_str):
                key = line_match.group(1).strip()
                value = line_match.group(2).strip()
                #out+="<tr><th>"+key+"</th><td>"+value+"</td></tr>"
                data[key] = value
            if data['name'] == '': continue
            if data['link'] == '':
                data['link'] = 'KIF440:' + data['name']
            data['link'] = re.sub(rx_link, '_', data['link'])
            try:
                the_ak = AK.objects.get(titel=data['name'])
                out += "<td>Update</td>"
            except AK.DoesNotExist:
                the_ak = AK.objects.create(titel=data['name'])
                out += "<td>Neu</td>"
            the_ak.__dict__.update(beschreibung=data['beschreibung'],
                    anzahl=data['wieviele'], leiter=data['wer'],
                    wann=data['wann'], dauer=data['dauer'], wiki_link=data['link'])
            out += "<td>"+data['name']+"</td>"
            the_ak.save()
            out += "</tr>"
            
        out+="</table>"
        
        return render(request, "oplan/ak_import_view.html", { 'titel': 'Raumliste importieren', 'output': out })



