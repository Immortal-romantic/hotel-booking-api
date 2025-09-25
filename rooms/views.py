from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Room
from decimal import Decimal, InvalidOperation

def error_response(message, status=400):
    """Возвращает JSON ответ с ошибкой"""
    return JsonResponse({"error": message}, status=status)

def success_response(data, status=200):
    """Возвращает успешный JSON ответ"""
    return JsonResponse(data, status=status)

@csrf_exempt
@require_http_methods(["POST"])
def create_room(request):
    """
    Создание нового номера отеля
    
    POST /rooms/create
    Параметры:
    - description: текстовое описание номера
    - price_per_night: цена за ночь (число)
    
    Возвращает:
    {"room_id": 1} - при успехе
    {"error": "текст ошибки"} - при ошибке
    """
    try:
        description = request.POST.get('description')
        price_per_night = request.POST.get('price_per_night')
        
        # Валидация данных
        if not description:
            return error_response("Поле 'description' обязательно")
        
        if not price_per_night:
            return error_response("Поле 'price_per_night' обязательно")
        
        # Проверка цены
        try:
            price = Decimal(price_per_night)
            if price <= 0:
                return error_response("Цена должна быть положительной")
        except (InvalidOperation, ValueError):
            return error_response("Неверный формат цены")
        
        # Создание номера
        room = Room.objects.create(
            description=description,
            price_per_night=price
        )
        
        return success_response({
            "room_id": room.id
        }, status=201)
    
    except Exception as e:
        return error_response(f"Внутренняя ошибка: {str(e)}", status=500)

@csrf_exempt
@require_http_methods(["POST"])
def delete_room(request):
    """
    Удаление номера отеля и всех его бронирований
    
    POST /rooms/delete
    Параметры:
    - room_id: ID номера для удаления
    
    Возвращает:
    {"message": "Номер удален"} - при успехе
    {"error": "текст ошибки"} - при ошибке
    """
    try:
        room_id = request.POST.get('room_id')
        
        if not room_id:
            return error_response("Поле 'room_id' обязательно")
        
        try:
            room_id = int(room_id)
        except ValueError:
            return error_response("Неверный формат room_id")
        
        # Находим номер
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return error_response("Номер не найден", status=404)
        
        # Удаляем номер (бронирования удалятся автоматически через CASCADE)
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
    """
    Получение списка номеров с сортировкой
    
    GET /rooms/list
    Параметры:
    - sort_by: поле для сортировки (price_per_night или created_at)
    - order: порядок сортировки (asc или desc)
    
    Возвращает:
    [{"room_id": 1, "description": "...", "price_per_night": "5000.00", "created_at": "..."}]
    """
    try:
        # Параметры сортировки
        sort_by = request.GET.get('sort_by', 'created_at')
        order = request.GET.get('order', 'asc')
        
        # Валидация параметров
        valid_sort_fields = ['price_per_night', 'created_at']
        if sort_by not in valid_sort_fields:
            return error_response(f"sort_by должно быть одним из: {valid_sort_fields}")
        
        if order not in ['asc', 'desc']:
            return error_response("order должно быть 'asc' или 'desc'")
        
        # Формирование запроса с сортировкой
        order_prefix = '' if order == 'asc' else '-'
        rooms = Room.objects.all().order_by(f'{order_prefix}{sort_by}')
        
        # Формирование данных для ответа
        rooms_data = []
        for room in rooms:
            rooms_data.append({
                "room_id": room.id,
                "description": room.description,
                "price_per_night": str(room.price_per_night),
                "created_at": room.created_at.isoformat(),
                "bookings_count": room.get_bookings_count()
            })
        
        return success_response(rooms_data)
    
    except Exception as e:
        return error_response(f"Внутренняя ошибка: {str(e)}", status=500)
