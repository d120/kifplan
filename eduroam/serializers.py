from rest_framework import serializers
from eduroam.models import GuestAccount

class GuestAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestAccount
