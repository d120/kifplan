from django.views.generic import View
from django.http import HttpResponse
from rest_framework import viewsets, permissions, filters
from django.contrib.auth.models import Group
from kiffel.models import Person
from kiffel.serializers import KiffelSerializer
from kiffel.helper import LaTeX, QueryFilter
from django.shortcuts import render

import datetime

from kiffel.helper import EAN8
from django.core.exceptions import PermissionDenied

import csv

class KiffelViewSet(viewsets.ModelViewSet):
    serializer_class = KiffelSerializer
    queryset = Person.objects.all()
    filter_fields = [f.name for f in Person._meta.get_fields()]
    search_fields = [f.name for f in Person._meta.get_fields()]
    ordering_fields = [f.name for f in Person._meta.get_fields()]


#//==> E X P O R T   F U N C T I O N S

class KiffelAttendingReport(View):
    """ automatic PDF export for attending reports """
    def get_queryset(self):
        queryset = Person.objects.all();
        return QueryFilter.filter(queryset, self.request, ['kiffel_id', 'hochschule', 'nickname'])

    def get(self, request, *args, **kwargs):
        items = LaTeX.escape(self.get_queryset())
        pdf = LaTeX.render(items, 'kiffel/attending-report.tex', ['bilder/KIFLogo-Schrift.jpg', 'scheine.sty'])
        r = HttpResponse(content_type='application/pdf')
        r['Content-Disposition'] = 'attachment; filename=kiffels-attending-reports.pdf'
        r.write(pdf)
        return r


class NametagsExport(View):
    """ automatic PDF export for nametags """
    def get_queryset(self):
        queryset = Person.objects.all();
        return QueryFilter.filter(queryset, self.request, ['kiffel_id', 'hochschule', 'ist_orga', 'nickname'])

    def get(self, request, *args, **kwargs):
        items = LaTeX.escape(self.get_queryset())
        pdf = LaTeX.render(items, 'kiffel/nametags.tex', ['bilder/kif_logo.png', 'namensschilder.sty'])
        r = HttpResponse(content_type='application/pdf')
        r['Content-Disposition'] = 'attachment; filename=kiffels-nametags.pdf'
        r.write(pdf)
        return r


class Schildergenerator(View):
    """ automatic Schildergenerator """
    def get(self, request, *args, **kwargs):
        data = {
            'headline': request.GET.get('headline'),
            'text': request.GET.get('text')
        }
        template = request.GET.get('template')
        pdf = LaTeX.render(data, 'schilder/'+template, ['bilder/kif_logo.png', 'schilder_style.tex'])
        r = HttpResponse(content_type='application/pdf')
        r['Content-Disposition'] = 'attachment; filename=schild.pdf'
        r.write(pdf)
        return r



#//==> I M P O R T   F U N C T I O N S

class ImportFromEngelsystem(View):
    def get(self, request, *args, **kwargs):
        foo = ""
        return render(request, "kiffel/import_csv_template.html", { 'titel': 'Import Engelsystem', 'output': '' })
    
    def updatePerson(self, person, engelid,nick,vorname,nachname,email,tshirt_groesse,kommentar,rollen,gruppen):
        person.engel_id = engelid
        if vorname != "": person.vorname = vorname
        if nachname != "": person.nachname = nachname
        if nick != "": person.nickname = nick
        if tshirt_groesse != "": person.tshirt_groesse = tshirt_groesse
        if kommentar != "": person.kommentar = kommentar
        
        groupNames = (rollen + '|' + gruppen).split('|')
        for gn in groupNames:
            if gn == "": continue
            try:
                g = Group.objects.get(name=gn)
                g.user_set.add(person)
            except Group.DoesNotExist :
                pass
        
        person.ist_orga = "Orga" in groupNames
        person.ist_helfer = True
        person.save()
    
    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('kiffel.import_persons'): raise PermissionDenied
        the_csv = request.POST["content"]
        reader = csv.reader(the_csv.splitlines())
        out = ""
        for row in reader:
            [engelid,nick,vorname,nachname,email,tshirt_groesse,kommentar,rollen,gruppen]=row
            if engelid == "ID": continue
            
            out += "<li><b><u>" + engelid + "</u> - " + email + "</b> (" + nick + " - "+vorname+" - "+nachname + ")<br>"
            p_by_id = Person.objects.filter(engel_id=engelid)
            if p_by_id.count() > 0:
                out += "Found by previously imported Engel ID<br>"
                self.updatePerson(p_by_id[0], engelid,nick,vorname,nachname,email,tshirt_groesse,kommentar,rollen,gruppen)
                continue
                
            
            p_by_mail = Person.objects.filter(email=email)
            if p_by_mail.count() > 0:
                out += "Found by EMAIL<br>"
                self.updatePerson(p_by_mail[0], engelid,nick,vorname,nachname,email,tshirt_groesse,kommentar,rollen,gruppen)
                continue
                
            out += "importing..."
            pneu = Person.objects.create(email=email, kdv_id=EAN8.get_random())
            pw = Person.objects.make_random_password()
            pneu.set_password(pw)
            
            self.updatePerson(pneu, engelid,nick,vorname,nachname,email,tshirt_groesse,kommentar,rollen,gruppen)
            out += "ok"
            out += "   created random pw="+pw
            
            
        return render(request, "kiffel/import_csv_template.html", { 'titel': 'Import Engelsystem', 'output': out })



class ImportFromKiffelAnmeldung(View):
    def get(self, request, *args, **kwargs):
        foo = ""
        return render(request, "kiffel/import_csv_template.html", { 'titel': 'Import KIF-Anmeldung', 'output': '' })
    
    def updatePerson(self, person, data):
        for key, value in data.items():
            setattr(person, key, value)
        person.save()
    
    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('kiffel.import_persons'):
            raise PermissionDenied
        the_csv = request.POST["content"]
        reader = csv.reader(the_csv.splitlines())
        out = ""
        for row in reader:
            data = dict(zip(anmeldung_csv_cols, row))
            if data["anmeldung_id"] == "#": continue
            
            data['ist_kiffel'] = True
            
            data['abreise_geplant'] = datetime.datetime.strptime(data['abreise_geplant'], '%d.%m.%Y')
            data['anreise_geplant'] = datetime.datetime.strptime(data['anreise_geplant'], '%d.%m.%Y')
            data['anmeldung_aktualisiert'] = datetime.datetime.strptime(data['anmeldung_aktualisiert'], '%Y-%m-%d %H:%M:%S %z')
            data['anmeldung_angelegt'] = datetime.datetime.strptime(data['anmeldung_angelegt'], '%Y-%m-%d %H:%M:%S %z')
            
            
            out += "<li><b><u>" + data["anmeldung_id"] + "</u> - " + data["email"] + "</b>  | " + data["nickname"] + " | "+data["vorname"]+" "+data["nachname"] + "<br>"
            p_by_id = Person.objects.filter(anmeldung_id=data["anmeldung_id"])
            if p_by_id.count() > 0:
                out += "Found by previously imported Anmeldung ID<br>"
                self.updatePerson(p_by_id[0], data)
                continue
                
            
            p_by_mail = Person.objects.filter(email=data["email"])
            if p_by_mail.count() > 0:
                out += "Found by EMAIL<br>"
                self.updatePerson(p_by_mail[0], data)
                continue
            
            
            out += "importing..."
            data['kdv_id'] = EAN8.get_random()
            pneu = Person.objects.create(**data)
            pw = Person.objects.make_random_password()
            pneu.set_password(pw); pneu.save()
            out += "ok"
            out += "   created random pw="+pw
            
        return render(request, "kiffel/import_csv_template.html", { 'titel': 'Import KIF-Anmeldung', 'output': out })

class CreateAnonymPerson(View):
    def get(self, request, *args, **kwargs):
        foo = ""
        return render(request, "kiffel/import_csv_template.html", { 'titel': 'Anonyme Accounts anlegen (bitte Anzahl eingeben)', 'output': '' })
    
    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('kiffel.import_persons'):
            raise PermissionDenied
        count = int(request.POST["content"])
        
        out = "Erstelle Anonyme Accounts "
        for i in range(count):
            barcode = EAN8.get_random()
            
            Person.objects.create(kdv_id=barcode,
                ist_anonym=True, nickname="zzz-anonym-"+barcode, email="zzz-anomym-"+barcode+"@example.com")
            out += "."
        
        out += "   OK"
        
        return render(request, "kiffel/import_csv_template.html", { 'titel': 'Import KIF-Anmeldung', 'output': out })



anmeldung_csv_cols = [
    "anmeldung_id",
    "vorname",
    "nachname",
    "email",
    "nickname",
    "student",
    "hochschule",
    "kommentar_public",
    "kommentar_orga",
    "anreise_geplant",
    "abreise_geplant",
    "ernaehrungsgewohnheit",
    "lebensmittelunvertraeglichkeiten",
    "volljaehrig",
    "eigener_schlafplatz",
    "tshirt_groesse",
    "nickname_auf_tshirt",
    "kapuzenjacke_groesse",
    "nickname_auf_kapuzenjacke",
    "weitere_tshirts",
    "interesse_theater",
    "interesse_esoc",
    "anmeldung_angelegt",
    "anmeldung_aktualisiert"
]




















