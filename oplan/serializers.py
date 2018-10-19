from rest_framework import serializers

from oplan.models import AK, Room, RoomAvailability, AKTermin


class AKSerializer(serializers.ModelSerializer):
    class Meta:
        model = AK
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAvailability
        fields = '__all__'


class AKTerminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AKTermin
        fields = '__all__'

    ak_titel = serializers.CharField(source='ak.titel', read_only=True)
    ak_color = serializers.CharField(source='ak.color', read_only=True)
    ak_constraints_freetext = serializers.CharField(source='ak.wann', read_only=True)
    


