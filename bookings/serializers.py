from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "room", "date_start", "date_end", "created_at")
        read_only_fields = ("id", "created_at")

    def validate(self, data):
        ds = data.get("date_start")
        de = data.get("date_end")
        if ds and de and ds >= de:
            raise serializers.ValidationError("date_start must be before date_end")
        return data
