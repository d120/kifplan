from django.shortcuts import render
from django.views.generic import View
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.db.models import Q

from django.core.urlresolvers import reverse

import datetime
from datetime import timedelta

from rest_framework import viewsets, permissions, filters

from oplan.models import AK, Room, RoomAvailability, AKTermin

from oplan.serializers import AKSerializer, RoomSerializer, RoomAvailabilitySerializer, AKTerminSerializer
import csv

# Views für die Planungsapp


#//==> A P I   V I E W S

class AKViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = AKSerializer
    queryset = AK.objects.all()
    filter_fields = [f.name for f in AK._meta.get_fields()]
    search_fields = [f.name for f in AK._meta.get_fields()]
    ordering_fields = [f.name for f in AK._meta.get_fields()]


class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    filter_fields = [f.name for f in Room._meta.get_fields()]
    search_fields = [f.name for f in Room._meta.get_fields()]
    ordering_fields = [f.name for f in Room._meta.get_fields()]


class AKTerminViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = AKTerminSerializer
    queryset = AKTermin.objects.all()
    filter_fields = [f.name for f in AKTermin._meta.get_fields()]
    search_fields = [f.name for f in AKTermin._meta.get_fields()]
    ordering_fields = [f.name for f in AKTermin._meta.get_fields()]
    def get_queryset(self):
        queryset = AKTermin.objects.all()
        only_unscheduled = self.request.query_params.get('only_unscheduled', False)
        if only_unscheduled:
            queryset = queryset.filter(Q(room__isnull=True) | Q(start_time__isnull=True))
        return queryset

class RoomAvailabilityViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = RoomAvailabilitySerializer
    queryset = RoomAvailability.objects.all()
    filter_fields = [f.name for f in RoomAvailability._meta.get_fields()]
    search_fields = [f.name for f in RoomAvailability._meta.get_fields()]
    ordering_fields = [f.name for f in RoomAvailability._meta.get_fields()]


	
class RoomAvailabilityApi(View):
    def get(self, request, *args, **kwargs):
        para = request.GET
        objs = RoomAvailability.objects.filter(start_time__range=[ para['start'], para['end'] ])
        if 'room' in para: objs = objs.filter(room__id=para['room'],)
        qq = []
        for obj in objs:
            qq.append({ 'avail_id': obj.id, 
                    'resourceId': obj.room.id,
                    'start': obj.start_time.astimezone().isoformat(),
                    'end': (obj.end_time).astimezone().isoformat(),
                    'title': obj.get_status_display() + " " + obj.kommentar,
                    'status': obj.status,
                    'kommentar': obj.kommentar,
                    'mgmt_id': obj.mgmt_id,
                    'edit_url': reverse('admin:oplan_roomavailability_change', args=[ obj.id ]),
                     })
        objs = AKTermin.objects.filter(start_time__range=[ para['start'], para['end'] ])
        if 'room' in para: objs = objs.filter(room__id=para['room'],)
        for obj in objs:
            qq.append({ 'termin_id': obj.id, 
                    'resourceId': obj.room.id,
                    'start': obj.start_time.astimezone().isoformat(),
                    'end': (obj.end_time).astimezone().isoformat(),
                    'title': obj.ak.titel,
                    'status': obj.status,
                    'kommentar': obj.kommentar,
                    'view_url': reverse('oplan:ak_details', args=[ obj.ak.id ]),
                    'edit_url': reverse('admin:oplan_aktermin_change', args=[ obj.id ]),
                    'edit_ak_url': reverse('admin:oplan_ak_change', args=[ obj.ak.id ]),
                     })
        return JsonResponse({ 'events' : qq,  })
        
    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.create_roomavailability'): raise PermissionDenied
        para = request.POST
        room = Room.objects.get(id=para['room'])
        startdt = parse_datetime(para['start'])
        enddt = parse_datetime(para['end'])
        if 'event_id' in para:
            obj = RoomAvailability.objects.get(id=para['event_id'])
        else:
            obj = RoomAvailability.objects.create(room=room, status=1, start_time = startdt, end_time=enddt)
        obj.start_time = startdt
        obj.end_time = enddt
        obj.room = room
        if 'status' in para: obj.status = para['status']
        if 'kommentar' in para: obj.kommentar = para['kommentar']
        
        obj.save()
        return JsonResponse({ 'success': 'true', 'id': obj.id })


#//==> I M P O R T    VIEWS

from oplan.dekrr_parser import getAllDekrrData
import re

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




class ImportDekrr(View):
    form_titel = 'Räume aus DEKRR importieren (bitte zu importierende Tage im Format yyyy-mm-dd angeben)'
    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.create_room'): raise PermissionDenied
        foo = ""
        return render(request, "oplan/ak_import_view.html", { 'titel': self.form_titel, 'output': '' })
    
    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.create_room'): raise PermissionDenied
        
        days = request.POST['content'].split('\n')
        out=""
        
        for day in days:
            day = day.strip()
            if day == "": continue
            dt = datetime.datetime.strptime(day, '%Y-%m-%d')
            out += "<h4>"+day+" = "+str(dt)+"</h4>"
            data = getAllDekrrData(dt)
            
            for dr in data:
                out += '<li>Raum "' + dr[0] + '" ...'
                try:
                    room = Room.objects.get(mgmt_id=dr[0], mgmt_source="DEKRR")
                    out += "found"
                except Room.DoesNotExist:
                    room = Room.objects.create(number=dr[0],
                        type='SR', capacity=dr[1], mgmt_id=dr[0], mgmt_source="DEKRR")
                    out += "created"
                
                out += "<ul>"
                RoomAvailability.objects.filter(room=room, mgmt_id__isnull=False, start_time__date=dt).delete()
                for avail in dr[2]:
                    RoomAvailability.objects.create(room=room,
                        start_time=avail['start_time'], end_time=avail['end_time'], 
                        kommentar=avail['kommentar'], mgmt_id=avail['mgmt_id'],
                        status=avail['status'].value)
                    out += "<li>" + str(avail['start_time']) + "  " + avail['kommentar']
                out += "</ul>"
        
        return render(request, "oplan/ak_import_view.html", { 'titel': self.form_titel, 'output': out })

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
                the_termin = AKTermin.objects.create(ak=the_ak,
                        status=3, # 3 = Not Scheduled
                        duration=timedelta(hours=2),
                        kommentar="")
                
                out += "<td>Neu</td>"
            the_ak.__dict__.update(beschreibung=data['beschreibung'],
                    anzahl=data['wieviele'], leiter=data['wer'],
                    wann=data['wann'], dauer=data['dauer'], wiki_link=data['link'])
            out += "<td>"+data['name']+"</td>"
            the_ak.save()
            out += "</tr>"
            
        out+="</table>"
        
        return render(request, "oplan/ak_import_view.html", { 'titel': 'Raumliste importieren', 'output': out })


#//==> REGULAR VIEWS

def roomcalendar(request, roomnumber, *args, **kwargs):
    room = Room.objects.get(number=roomnumber)
    return render(request, "oplan/roomcalendar.html", { 'titel': 'Rauminfo '+room.number, 'room': room })


def oplan_home(request, *args, **kwargs):
    return render(request, "oplan/ak_import_view.html", { 'titel': 'Moin moin', 'out': '',  })

def ak_details(request, akid, *args, **kwargs):
    ak = AK.objects.get(id=akid)
    return render(request, "oplan/ak_import_view.html", { 'titel': ak.titel, 'content': ak.beschreibung })

def ak_wall(request, *args, **kwargs):
    return render(request, "oplan/akwallcalendar.html", { 'titel': 'AK Wall',  })

def infoscreen(request, *args, **kwargs):
    now = datetime.datetime.now()
    if 'now' in request.GET: now = datetime.datetime.strptime(request.GET['now'], '%y-%m-%d-%H-%M')
    
    current = AKTermin.objects.filter(start_time__lte=now, end_time__gte=now)
    upcoming = AKTermin.objects.filter(start_time__gte=now, start_time__lte=now+timedelta(hours=2))
    
    return render(request, "oplan/infoscreen.html", { 'titel': 'Infoscreen ', 'now': now, 'current_akts': current, 'upcoming_akts': upcoming })

def darwin_status(request, *args, **kwargs):
    return render(request, "oplan/ak_import_view.html", { 'titel': 'TODO: Automatische AK-Zuordnung ("Darwin") - Status ', 'out': '' })



