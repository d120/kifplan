from django.shortcuts import render,redirect
from django.views.generic import View
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
#from django.http.shortcuts import redirect

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
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    serializer_class = AKSerializer
    queryset = AK.objects.all()
    filter_fields = [f.name for f in AK._meta.get_fields()]
    search_fields = [f.name for f in AK._meta.get_fields()]
    ordering_fields = [f.name for f in AK._meta.get_fields()]


class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    filter_fields = [f.name for f in Room._meta.get_fields()]
    search_fields = [f.name for f in Room._meta.get_fields()]
    ordering_fields = [f.name for f in Room._meta.get_fields()]


class AKTerminViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
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
                    'ak_color': obj.ak.color
                     })
        return JsonResponse({ 'events' : qq,  })
        
    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.add_roomavailability'): raise PermissionDenied
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
        if not request.user.has_perm('oplan.add_room'): raise PermissionDenied
        foo = ""
        return render(request, "oplan/ak_import_view.html", { 'title': 'Raumliste importieren (Format: "Raumnummer,Kapazität")', 'output': '' })
    
    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.add_room'): raise PermissionDenied
        
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
        
        return render(request, "oplan/ak_import_view.html", { 'title': 'Raumliste importieren', 'output': out })




class ImportDekrr(View):
    form_titel = 'Räume aus DEKRR importieren (bitte zu importierende Tage im Format yyyy-mm-dd angeben)'
    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.add_room'): raise PermissionDenied
        foo = ""
        return render(request, "oplan/ak_import_view.html", { 'title': self.form_titel, 'output': '' })
    
    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.add_room'): raise PermissionDenied
        
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
        
        return render(request, "oplan/ak_import_view.html", { 'title': self.form_titel, 'output': out })

from random import randint
def hextodec(color):
    if color[0] == '#':
        color = color[1:]
    assert(len(color) == 6)
    return int(color[:2], 16), int(color[2:4], 16), int(color[4:6], 16)
def dectohex(rgb):
    return '#%02x%02x%02x' % rgb

def random_similar_color(mix):
    mix = hextodec(mix)
    (r,g,b) = (randint(0,255), randint(0,255), randint(0,255))
    r = (r + 2*mix[0]) / 3
    g = (g + 2*mix[1]) / 3
    b = (b + 2*mix[2]) / 3
    return dectohex((r,g,b))

class ImportWikiAkListe(View):
    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.add_room'): raise PermissionDenied
        foo = ""
        return render(request, "oplan/ak_import_view.html", { 'title': 'AKs importieren (Quelltext der Wikiseite hier pasten)', 'output': '' })
    
    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('oplan.add_room'): raise PermissionDenied
        
        wikitext = request.POST["content"]
        
        rx = re.compile(r"""
        (?:
        ^==+\s*(?P<headline>[^\n]+)\s=+=\s*$
        |
        ^\s*\{\{Ak\sSpalte[\sa-z0-9]*
        (?P<ak_str>.*?)
        ^\s*\}\}
        )
        """, re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE)
        rx2 = re.compile(r"""
        ^\|\s*([a-z]+)\s*=(.*?)$
        """, re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE)
        rx_link = re.compile(r"\s+")
        
        out="Ergebnis:"
        out+="<table>"
        headline = ""
        color = "#ff00ff"
        for ak_match in rx.finditer(wikitext):
            if ak_match.group('headline'):
                headline = ak_match.group('headline')
                out += "<tr><td colspan=3>"+headline+"</td></tr>"
                if 'Inhalt' in headline: color = "#1122ff"
                if 'Kultur' in headline: color = "#22ff00"
                continue
            
            ak_color = random_similar_color(color)
            out += "<tr><td bgcolor='"+ak_color+"'></td>"
            ak_str = ak_match.group('ak_str')
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
                the_ak = AK.objects.create(titel=data['name'], color=ak_color)
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
        
        return render(request, "oplan/ak_import_view.html", { 'title': 'Raumliste importieren', 'output': out })


#//==> REGULAR VIEWS

def roomcalendar(request, roomnumber, *args, **kwargs):
    room = Room.objects.get(number=roomnumber)
    return render(request, "oplan/roomcalendar.html", { 'title': 'Rauminfo '+room.number, 'room': room })

def roomlist(request, *args, **kwargs):
    return render(request, "oplan/roomlist.html", { 'title': 'Raumliste', 'rooms': Room.objects.all() })

def aklist(request, *args, **kwargs):
    return render(request, "oplan/aklist.html", { 'title': 'AK-Liste', 'aks': AK.objects.all() })


def oplan_home(request, *args, **kwargs):
    return redirect('oplan:ak_wall')

def ak_details(request, akid, *args, **kwargs):
    ak = AK.objects.get(id=akid)
    return render(request, "oplan/ak_details_view.html", { 'title': "AK-Details", 'ak': ak })

def ak_wall(request, *args, **kwargs):
    return render(request, "oplan/akwallcalendar.html", { 'title': 'AK Wall', 'beamer': False })

def ak_wall_beamer(request, *args, **kwargs):
    akts = AKTermin.objects.all().order_by('start_time')
    rooms = Room.objects.all().order_by('number')
    return render(request, "oplan/akwallbeamer.html", { 'title': 'AK Wall', 'termine': akts, 'rooms': rooms  })

def akcalendar(request, *args, **kwargs):
    return render(request, "oplan/akwallcalendar.html", { 'title': 'AK Kalender',  })

def akbeamer(request, *args, **kwargs):
    return render(request, "oplan/akbeamer.html", { 'title': 'AK Wall',  })

def infoscreen(request, *args, **kwargs):
    now = datetime.datetime.now()
    if 'now' in request.GET: now = datetime.datetime.strptime(request.GET['now'], '%y-%m-%d-%H-%M')

    current = AKTermin.objects.filter(start_time__lte=now, end_time__gte=now)
    upcoming = AKTermin.objects.filter(start_time__gte=now, start_time__lte=now+timedelta(hours=2))

    return render(request, "oplan/infoscreen.html", {
        'title': 'Infoscreen ', 'now': now,
        'current_akts': current, 'upcoming_akts': upcoming,
        'beamer': False
    })

def infoscreen_beamer(request, *args, **kwargs):
    now = datetime.datetime.now()
    if 'now' in request.GET: now = datetime.datetime.strptime(request.GET['now'], '%y-%m-%d-%H-%M')

    current = AKTermin.objects.filter(start_time__lte=now, end_time__gte=now)
    upcoming = AKTermin.objects.filter(start_time__gte=now, start_time__lte=now+timedelta(hours=2))

    return render(request, "oplan/infoscreen.html", {
        'title': 'Infoscreen ', 'now': now,
        'current_akts': current, 'upcoming_akts': upcoming,
        'beamer': True
    })

def darwin_status(request, *args, **kwargs):
    return render(request, "oplan/ak_import_view.html", { 'title': 'TODO: Automatische AK-Zuordnung ("Darwin") - Status ', 'out': '' })



