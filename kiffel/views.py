from django.views.generic import ListView
from rest_framework import viewsets, permissions

from kiffel.models import Kiffel
from kiffel.serializers import KiffelSerializer


class KiffelViewSet(viewsets.ModelViewSet):
    serializer_class = KiffelSerializer
    queryset = Kiffel.objects.all()


class KiffelAttendingReport(ListView):
    template_name = 'kiffel/attending-report.tex'
    context_object_name = 'kiffels'

    def get_queryset(self):
        queryset = Kiffel.objects.all();
        kiffel_id = self.request.GET.get('kiffel_id', None)
        if kiffel_id is not None:
            queryset = queryset.filter(id=kiffel_id)
        hochschule = self.request.GET.get('hochschule', None)
        if hochschule is not None:
            queryset = queryset.filter(hochschule=hochschule)
        return queryset
