from rest_framework import serializers
from kiffel.models import Kiffel

class KiffelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiffel
