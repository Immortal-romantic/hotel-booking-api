from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer


@api_view(["POST"])
def create_room(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        room = serializer.save()
        return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_rooms(request):
    sort_by = request.GET.get("sort_by", "created_at")
    order = request.GET.get("order", "asc")

    valid_sort_fields = ["price", "created_at"]
    if sort_by not in valid_sort_fields:
        return Response(
            {"error": f"sort_by должно быть одним из: {valid_sort_fields}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if order not in ["asc", "desc"]:
        return Response(
            {"error": "order должно быть 'asc' или 'desc'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    order_prefix = "" if order == "asc" else "-"
    rooms = Room.objects.all().order_by(f"{order_prefix}{sort_by}")

    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response({"error": "Номер не найден"}, status=status.HTTP_404_NOT_FOUND)

    room.delete()
    return Response(
        {"message": f"Номер {room_id} удалён"}, status=status.HTTP_204_NO_CONTENT
    )
