from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from .models import Booking
from rooms.models import Room
from datetime import datetime

def error_response(message, status=400):
    return JsonResponse({"error": message}, status=status)

def success_response(data, status=200):
    return JsonResponse(data, status=status)

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError(f"Дата '{date_string}' должна быть в формате YYYY-MM-DD")

@csrf_exempt
@require_http_methods(["POST"])
def create_booking(request):
    """
    Создание нового бронирования
    
    POST /bookings/create
    Параметры:
    - room_id: ID существующего номера отеля
    - date_start: дата начала бронирования (YYYY-MM-DD)
    - date_end: дата окончания бронирования (YYYY-MM-DD)
    
    Возвращает:
    {"booking_id": 1} - при успехе
    {"error": "текст ошибки"} - при ошибке
    """
    try:
        room_id = request.POST.get('room_id')
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('date_end')
        
        if not room_id:
            return error_response("Поле 'room_id' обязательно")
        if not date_start:
            return error_response("Поле 'date_start' обязательно")
        if not date_end:
            return error_response("Поле 'date_end' обязательно")
        
        try:
            room_id = int(room_id)
        except ValueError:
            return error_response("Неверный формат room_id")
        
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return error_response("Номер не найден", status=404)
        
        try:
            date_start_parsed = parse_date(date_start)
            date_end_parsed = parse_date(date_end)
        except ValueError as e:
            return error_response(str(e))
        

        booking = Booking(
            room=room,
            date_start=date_start_parsed,
            date_end=date_end_parsed
        )
        
        try:
            booking.clean()
            
            if not booking.check_availability():
                return error_response(
                    f"Номер уже забронирован на период с {date_start} по {date_end}"
                )
            
            booking.save()
            
        except ValidationError as e:
            error_messages = e.messages if hasattr(e, 'messages') else [str(e)]
            return error_response('; '.join(error_messages))
        
        return success_response({
            "booking_id": booking.id
        }, status=201)
    
    except Exception as e:
        return error_response(f"Внутренняя ошибка: {str(e)}", status=500)

@csrf_exempt
@require_http_methods(["POST"])
def delete_booking(request):
    """
    Удаление бронирования
    
    POST /bookings/delete
    Параметры:
    - booking_id: ID бронирования для удаления
    
    Возвращает:
    {"message": "Бронирование удалено"} - при успехе
    {"error": "текст ошибки"} - при ошибке
    """
    try:
        booking_id = request.POST.get('booking_id')
        
        if not booking_id:
            return error_response("Поле 'booking_id' обязательно")
        
        try:
            booking_id = int(booking_id)
        except ValueError:
            return error_response("Неверный формат booking_id")
        
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return error_response("Бронирование не найдено", status=404)
        
        booking.delete()
        
        return success_response({
            "message": f"Бронирование {booking_id} удалено"
        })
    
    except Exception as e:
        return error_response(f"Внутренняя ошибка: {str(e)}", status=500)

@require_http_methods(["GET"])
def list_bookings(request):
    """
    Получение списка бронирований номера отеля
    
    GET /bookings/list?room_id=X
    Параметры:
    - room_id: ID номера отеля
    
    Возвращает:
    [{"booking_id": 1, "date_start": "2023-12-01", "date_end": "2023-12-05"}]
    """
    try:
        room_id = request.GET.get('room_id')
        
        if not room_id:
            return error_response("Параметр 'room_id' обязателен")
        
        try:
            room_id = int(room_id)
        except ValueError:
            return error_response("Неверный формат room_id")
        
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return error_response("Номер не найден", status=404)
        
        bookings = Booking.objects.filter(room=room).order_by('date_start')
        
        bookings_data = []
        for booking in bookings:
            bookings_data.append({
                "booking_id": booking.id,
                "date_start": booking.date_start.strftime('%Y-%m-%d'),
                "date_end": booking.date_end.strftime('%Y-%m-%d'),
                "duration_days": booking.get_duration_days()
            })
        
        return success_response(bookings_data)
    
    except Exception as e:
        return error_response(f"Внутренняя ошибка: {str(e)}", status=500)
