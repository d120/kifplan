from rest_framework import viewsets, permissions, filters

from eduroam.models import GuestAccount
from eduroam.serializers import GuestAccountSerializer


class GuestAccountViewSet(viewsets.ModelViewSet):
    serializer_class = GuestAccountSerializer
    queryset = GuestAccount.objects.all()
    filter_fields = [f.name for f in GuestAccount._meta.get_fields()]
    search_fields = [f.name for f in GuestAccount._meta.get_fields()]
    ordering_fields = [f.name for f in GuestAccount._meta.get_fields()]
