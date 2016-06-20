from rest_framework import serializers

from oplan.models import AK, Room, RoomAvailability, AKTermin

class AKSerializer(serializers.ModelSerializer):
    class Meta:
        model = AK
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
class RoomAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAvailability
class AKTerminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AKTermin
    ak_titel = serializers.CharField(source='ak.titel', read_only=True)
    ak_color = serializers.CharField(source='ak.color', read_only=True)
    ak_constraints_freetext = serializers.CharField(source='ak.wann', read_only=True)
    


