from rest_framework import serializers

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Room
        fields = ("room_id", "description", "price", "created_at")
        read_only_fields = ("room_id", "created_at")
