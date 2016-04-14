from django.views.generic import View
from django.http import HttpResponse
from rest_framework import viewsets, permissions, filters

from kiffel.models import Person
from kiffel.serializers import KiffelSerializer
from kiffel.helper import LaTeX, QueryFilter
from django.shortcuts import render

import csv

class KiffelViewSet(viewsets.ModelViewSet):
    serializer_class = KiffelSerializer
    queryset = Person.objects.all()
    filter_fields = [f.name for f in Person._meta.get_fields()]
    search_fields = [f.name for f in Person._meta.get_fields()]
    ordering_fields = [f.name for f in Person._meta.get_fields()]


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


class ImportFromEngelsystem(View):
    def get(self, request, *args, **kwargs):
        foo = ""
        return render(request, "kiffel/import_csv_template.html")

    def post(self, request, *args, **kwargs):
        the_csv = request.POST["content"]
        reader = csv.reader(the_csv.splitlines())
        out = ""
        for row in reader:
            [engelid,nick,vorname,nachname,email,tshirt_groesse,kommentar]=row
            if engelid == "ID": continue
            
            out += "<li><b><u>" + engelid + "</u> - " + email + "</b> (" + nick + " - "+vorname+" - "+nachname + ")<br>"
            p_by_id = Person.objects.filter(engel_id=engelid)
            if p_by_id.count() > 0:
                out += "Found by previously imported Engel ID<br>"
                continue
                
            
            p_by_mail = Person.objects.filter(email=email)
            if p_by_mail.count() > 0:
                out += "Found by EMAIL<br>"
                continue
                
            out += "would import"
            
        return HttpResponse(out)






















