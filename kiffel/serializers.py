from rest_framework import serializers
from kiffel.models import Person

class KiffelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

