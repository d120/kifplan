from rest_framework import serializers

from oplan.models import AK, Room, RoomOpening

class AKSerializer(serializers.ModelSerializer):
    class Meta:
        model = AK
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
class RoomOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomOpening


