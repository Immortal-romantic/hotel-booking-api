from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rooms.models import Room

from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.GenericViewSet):
    queryset = Booking.objects.all().order_by("date_start")
    serializer_class = BookingSerializer

    @action(detail=False, methods=["post"], url_path="create")
    def create_booking(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = serializer.validated_data["room"]
        date_start = serializer.validated_data["date_start"]
        date_end = serializer.validated_data["date_end"]

        with transaction.atomic():
            room_locked = Room.objects.select_for_update().filter(pk=room.pk).first()
            if not room_locked:
                return Response(
                    {"error": "room not found"}, status=status.HTTP_404_NOT_FOUND
                )
            overlap = room_locked.bookings.filter(
                date_start__lt=date_end, date_end__gt=date_start
            ).exists()
            if overlap:
                return Response(
                    {"error": "room not available for given dates"},
                    status=status.HTTP_409_CONFLICT,
                )
            b = Booking.objects.create(
                room=room_locked, date_start=date_start, date_end=date_end
            )
        return Response({"booking_id": b.id}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="list")
    def list_by_room(self, request):
        room_id = request.query_params.get("room_id")
        if not room_id:
            return Response(
                {"error": "room_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        qs = Booking.objects.filter(room_id=room_id).order_by("date_start")
        serializer = BookingSerializer(qs, many=True)
        return Response(serializer.data)
