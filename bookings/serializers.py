from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='id', read_only=True)  # ← изменить на booking_id

    class Meta:
        model = Booking
        fields = ("booking_id", "room", "date_start", "date_end", "created_at")
        read_only_fields = ("booking_id", "created_at")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['room_id'] = instance.room.id
        del data['room']
        return data

    def validate(self, data):
        ds = data.get("date_start")
        de = data.get("date_end")
        if ds and de and ds >= de:
            raise serializers.ValidationError("date_start must be before date_end")
        return data
