from django.views.generic import ListView, View
from django.http import HttpResponse
from rest_framework import viewsets, permissions, filters

from kiffel.models import Kiffel
from kiffel.serializers import KiffelSerializer
from kiffel.helper import LaTeX


class KiffelViewSet(viewsets.ModelViewSet):
    serializer_class = KiffelSerializer
    queryset = Kiffel.objects.all()
    filter_fields = [f.name for f in Kiffel._meta.get_fields()]
    search_fields = [f.name for f in Kiffel._meta.get_fields()]
    ordering_fields = [f.name for f in Kiffel._meta.get_fields()]


class KiffelAttendingReport(ListView):
    """
    automatic PDF export for attending reports
    """

    def get_queryset(self):
        queryset = Kiffel.objects.all();
        kiffel_id = self.request.GET.get('kiffel_id', None)
        hochschule = self.request.GET.get('hochschule', None)
        nickname = self.request.GET.get('nickname', None)
        if kiffel_id is not None:
            queryset = queryset.filter(id=kiffel_id)
        if hochschule is not None:
            queryset = queryset.filter(hochschule=hochschule)
        if nickname is not None:
            queryset = queryset.filter(nickname=nickname)
        return queryset

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
        kiffel_id = self.request.GET.get('kiffel_id', None)
        hochschule = self.request.GET.get('hochschule', None)
        ist_orga = self.request.GET.get('ist_orga', None)
        nickname = self.request.GET.get('nickname', None)
        if kiffel_id is not None:
            queryset = queryset.filter(id=kiffel_id)
        if hochschule is not None:
            queryset = queryset.filter(hochschule=hochschule)
        if ist_orga is not None:
            queryset = queryset.filter(ist_orga=ist_orga)
        if nickname is not None:
            queryset = queryset.filter(nickname=nickname)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        pdf = LaTeX.render(queryset, 'kiffel/nametags.tex', ['kif_logo.png', 'kifschilder.sty'])
        r = HttpResponse(content_type='application/pdf')
        r['Content-Disposition'] = 'attachment; filename=kiffels-nametags.pdf'
        r.write(pdf)
        return r
