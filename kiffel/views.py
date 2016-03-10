from django.views.generic import View
from django.http import HttpResponse
from rest_framework import viewsets, permissions, filters

from kiffel.models import Kiffel
from kiffel.serializers import KiffelSerializer
from kiffel.helper import LaTeX, QueryFilter


class KiffelViewSet(viewsets.ModelViewSet):
    serializer_class = KiffelSerializer
    queryset = Kiffel.objects.all()
    filter_fields = [f.name for f in Kiffel._meta.get_fields()]
    search_fields = [f.name for f in Kiffel._meta.get_fields()]
    ordering_fields = [f.name for f in Kiffel._meta.get_fields()]


class KiffelAttendingReport(View):
    """ automatic PDF export for attending reports """
    def get_queryset(self):
        queryset = Kiffel.objects.all();
        return QueryFilter.filter(queryset, self.request, ['kiffel_id', 'hochschule', 'nickname'])

    def get(self, request, *args, **kwargs):
        items = LaTeX.escape(self.get_queryset())
        pdf = LaTeX.render(items, 'kiffel/attending-report.tex', ['KIFLogo-Schrift.jpg', 'scheine.sty'])
        r = HttpResponse(content_type='application/pdf')
        r['Content-Disposition'] = 'attachment; filename=kiffels-attending-reports.pdf'
        r.write(pdf)
        return r


class NametagsExport(View):
    """ automatic PDF export for nametags """
    def get_queryset(self):
        queryset = Kiffel.objects.all();
        return QueryFilter.filter(queryset, self.request, ['kiffel_id', 'hochschule', 'ist_orga', 'nickname'])

    def get(self, request, *args, **kwargs):
        items = LaTeX.escape(self.get_queryset())
        pdf = LaTeX.render(items, 'kiffel/nametags.tex', ['kif_logo.png', 'namensschilder.sty'])
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
        pdf = LaTeX.render(data, 'kiffel/'+template, ['kif_logo.png'])
        r = HttpResponse(content_type='application/pdf')
        r['Content-Disposition'] = 'attachment; filename=schild.pdf'
        r.write(pdf)
        return r
