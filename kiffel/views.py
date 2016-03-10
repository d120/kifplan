from django.views.generic import ListView, View
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from rest_framework import viewsets, permissions, filters

import io, tempfile, os, shutil
from subprocess import Popen, PIPE

from kiffel.models import Kiffel
from kiffel.serializers import KiffelSerializer


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

    def escape(self, queryset):
        for kiffel in queryset:
            for key, value in kiffel.__dict__.items():
                if isinstance(value, str):
                    kiffel.__dict__[key] = value.replace('_', '\_')
        return queryset

    def get(self, request, *args, **kwargs):
        kiffels = self.escape(self.get_queryset())
        template = get_template('kiffel/attending-report.tex')
        rendered_tpl = template.render({'kiffels': kiffels}).encode('utf-8')
        with tempfile.TemporaryDirectory() as tempdir:
            shutil.copy(os.path.dirname(os.path.realpath(__file__))+'/assets/KIFLogo-Schrift.jpg', tempdir)
            shutil.copy(os.path.dirname(os.path.realpath(__file__))+'/assets/scheine.sty', tempdir)
            for i in range(2):
                process = Popen(
                    ['pdflatex'],
                    stdin=PIPE,
                    stdout=PIPE,
                    cwd=tempdir,
                )
                process.communicate(rendered_tpl)
            with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
                pdf = f.read()
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

    def escape(self, queryset):
        for kiffel in queryset:
            for key, value in kiffel.__dict__.items():
                if isinstance(value, str):
                    kiffel.__dict__[key] = value.replace('_', '\_')
        return queryset

    def get(self, request, *args, **kwargs):
        kiffels = self.escape(self.get_queryset())
        template = get_template('kiffel/nametags.tex')
        rendered_tpl = template.render({'kiffels': kiffels}).encode('utf-8')
        with tempfile.TemporaryDirectory() as tempdir:
            shutil.copy(os.path.dirname(os.path.realpath(__file__))+'/assets/kif_logo.png', tempdir)
            shutil.copy(os.path.dirname(os.path.realpath(__file__))+'/assets/kifschilder.sty', tempdir)
            for i in range(2):
                process = Popen(
                    ['pdflatex'],
                    stdin=PIPE,
                    stdout=PIPE,
                    cwd=tempdir,
                )
                process.communicate(rendered_tpl)
            with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
                pdf = f.read()
        r = HttpResponse(content_type='application/pdf')
        r['Content-Disposition'] = 'attachment; filename=kiffels-nametags.pdf'
        r.write(pdf)
        return r
