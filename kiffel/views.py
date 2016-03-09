from django.views.generic import ListView, View
from django.http import HttpResponse
from rest_framework import viewsets, permissions, filters

import io, odswriter

from kiffel.models import Kiffel
from kiffel.serializers import KiffelSerializer


class KiffelViewSet(viewsets.ModelViewSet):
    serializer_class = KiffelSerializer
    queryset = Kiffel.objects.all()
    filter_fields = tuple(Kiffel._meta.get_all_field_names())
    search_fields = tuple(Kiffel._meta.get_all_field_names())
    ordering_fields = tuple(Kiffel._meta.get_all_field_names())


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


class NametagsOdsExport(View):
    """
    TODO: Dieser Export verwendet das Format für Namensschilder der Ophase.
    Da für die KIF weitere Felder notwendig sind, muss dies hier angepasst werden!
    """

    def get(self, request):
        """
        Exports certain staff data in ods format, containing the necessary information for the name tag production application. The produced ods file is the input for the name tag Java aplication.
        """

        table = []
        empty = '~'

        for kiffel in Kiffel.objects.all():
            row = [kiffel.nickname, '', 'K', 'KIFFEL', 'ORGA']
            row.extend([empty]*4)
            table.append(row)

        out_stream = io.BytesIO()
        with odswriter.writer(out_stream) as out:
            # need to specify number of columns for jOpenDocument compatibility
            sheet = out.new_sheet("Staff", cols=9)
            sheet.writerows(table)

        response = HttpResponse(out_stream.getvalue(), content_type="application/vnd.oasis.opendocument.spreadsheet")
        # name the file according to the expectations of the Java name tag application
        response['Content-Disposition'] = 'attachment; filename="kiffels.ods"'
        return response
