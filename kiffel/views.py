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
    """
    automatic PDF export for attending reports
    """

    def get_queryset(self):
        queryset = Kiffel.objects.all();
        return QueryFilter.filter(queryset, self.request, ['kiffel_id', 'hochschule', 'nickname'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        pdf = LaTeX.render(queryset, 'kiffel/attending-report.tex', ['KIFLogo-Schrift.jpg', 'scheine.sty'])
        r = HttpResponse(content_type='application/pdf')
        r['Content-Disposition'] = 'attachment; filename=kiffels-attending-reports.pdf'
        r.write(pdf)
        return r


class NametagsExport(View):
    """
    automatic PDF export for nametags
    """

    def get_queryset(self):
        queryset = Kiffel.objects.all();
        return QueryFilter.filter(queryset, self.request, ['kiffel_id', 'hochschule', 'ist_orga', 'nickname'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        pdf = LaTeX.render(queryset, 'kiffel/nametags.tex', ['kif_logo.png', 'kifschilder.sty'])
        r = HttpResponse(content_type='application/pdf')
        r['Content-Disposition'] = 'attachment; filename=kiffels-nametags.pdf'
        r.write(pdf)
        return r
