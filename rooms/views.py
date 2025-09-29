from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Room
from decimal import Decimal, InvalidOperation
import json

def error_response(message, status=400):
    return JsonResponse({"error": message}, status=status)

def success_response(data, status=200):
    return JsonResponse(data, status=status)

@csrf_exempt
@require_http_methods(["POST"])
def create_room(request):
    try:
        content_type = request.META.get('CONTENT_TYPE', '')
        
        if 'application/json' in content_type:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return error_response("Неверный формат JSON", 400)
            
            description = data.get('description')
            price = data.get('price')  # ← Вот тут: было price_per_night
        else:
            description = request.POST.get('description')
            price = request.POST.get('price')  # ← Вот тут: было price_per_night
        
        if not description:
            return error_response("Поле 'description' обязательно")
        
        if not price:
            return error_response("Поле 'price' обязательно")  # ← Обнови сообщение
        
        try:
            price_decimal = Decimal(price)
            if price_decimal <= 0:
                return error_response("Цена должна быть положительной")
        except (InvalidOperation, ValueError):
            return error_response("Неверный формат цены")
        
        room = Room.objects.create(
            description=description,
            price=price_decimal  # ← Вот тут: было price_per_night
        )
        
        return success_response({
            "room_id": room.id
        }, status=201)
    
    except Exception as e:
        return error_response(f"Внутренняя ошибка: {str(e)}", status=500)

@csrf_exempt
@require_http_methods(["POST"])
def delete_room(request):
    try:
        room_id = request.POST.get('room_id')
        
        if not room_id:
            return error_response("Поле 'room_id' обязательно")
        
        try:
            room_id = int(room_id)
        except ValueError:
            return error_response("Неверный формат room_id")
        
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return error_response("Номер не найден", status=404)
        
        with transaction.atomic():
            bookings_count = room.get_bookings_count()
            room.delete()
        
        return success_response({
            "message": f"Номер {room_id} и {bookings_count} бронирований удалены"
        })
    
    except Exception as e:
        return error_response(f"Внутренняя ошибка: {str(e)}", status=500)

@require_http_methods(["GET"])
def list_rooms(request):
    try:
        sort_by = request.GET.get('sort_by', 'created_at')
        order = request.GET.get('order', 'asc')
        
        valid_sort_fields = ['price', 'created_at']  # ← Обнови: было price_per_night
        if sort_by not in valid_sort_fields:
            return error_response(f"sort_by должно быть одним из: {valid_sort_fields}")
        
        if order not in ['asc', 'desc']:
            return error_response("order должно быть 'asc' или 'desc'")
        
        order_prefix = '' if order == 'asc' else '-'
        rooms = Room.objects.all().order_by(f'{order_prefix}{sort_by}')
        
        rooms_data = []
        for room in rooms:
            rooms_data.append({
                "room_id": room.id,
                "description": room.description,
                "price": str(room.price),  # ← Обнови: было price_per_night
                "created_at": room.created_at.isoformat(),
                "bookings_count": room.get_bookings_count()
            })
        
        return success_response(rooms_data)
    
    except Exception as e:
        return error_response(f"Внутренняя ошибка: {str(e)}", status=500)