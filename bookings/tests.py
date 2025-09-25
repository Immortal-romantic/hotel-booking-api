# rooms/tests.py
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from .models import Room, Booking
from decimal import Decimal
from datetime import date, timedelta
import json


class RoomModelTest(TestCase):
    """Тесты модели Room"""
    
    def test_room_creation(self):
        """Тест создания номера"""
        room = Room.objects.create(
            description="Люкс с видом на море",
            price_per_night=Decimal('5000.00')
        )
        self.assertEqual(room.description, "Люкс с видом на море")
        self.assertEqual(room.price_per_night, Decimal('5000.00'))
        self.assertTrue(room.created_at)
    
    def test_room_str(self):
        """Тест строкового представления номера"""
        room = Room.objects.create(
            description="Стандартный номер",
            price_per_night=Decimal('3000.00')
        )
        self.assertIn(str(room.price_per_night), str(room))


class BookingModelTest(TestCase):
    """Тесты модели Booking"""
    
    def setUp(self):
        self.room = Room.objects.create(
            description="Тестовый номер",
            price_per_night=Decimal('2000.00')
        )
        self.today = date.today()
        self.tomorrow = self.today + timedelta(days=1)
        self.day_after_tomorrow = self.today + timedelta(days=2)
    
    def test_booking_creation(self):
        """Тест создания бронирования"""
        booking = Booking.objects.create(
            room=self.room,
            date_start=self.tomorrow,
            date_end=self.day_after_tomorrow
        )
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.date_start, self.tomorrow)
        self.assertEqual(booking.date_end, self.day_after_tomorrow)
    
    def test_booking_validation_end_before_start(self):
        """Тест валидации: дата окончания раньше даты начала"""
        booking = Booking(
            room=self.room,
            date_start=self.day_after_tomorrow,
            date_end=self.tomorrow
        )
        with self.assertRaises(ValidationError):
            booking.clean()
    
    def test_booking_validation_past_date(self):
        """Тест валидации: нельзя бронировать на прошедшие даты"""
        yesterday = self.today - timedelta(days=1)
        booking = Booking(
            room=self.room,
            date_start=yesterday,
            date_end=self.tomorrow
        )
        with self.assertRaises(ValidationError):
            booking.clean()
    
    # def test_booking_availability_check(self):
    #     """Тест проверки доступности номера"""
    #     # Создаем первое бронирование
    #     booking1 = Booking.objects.create(
    #         room=self.room,
    #         date_start=self.tomorrow,
    #         date_end=self.day_after_tomorrow
    #     )
        
        # Пытаемся создать пересекающееся бронирование
        booking2 = Booking(
            room=self.room,
            date_start=self.tomorrow,
            date_end=self.day_after_tomorrow + timedelta(days=1)
        )
        
        self.assertFalse(booking2.check_availability())


class RoomAPITest(TestCase):
    """Тесты API для номеров"""
    
    def setUp(self):
        self.client = Client()
    
    def test_create_room_success(self):
        """Тест успешного создания номера"""
        response = self.client.post('/rooms/create', {
            'description': 'Стандартный номер',
            'price_per_night': '3000.00'
        })
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertIn('room_id', data)
        
        room = Room.objects.get(id=data['room_id'])
        self.assertEqual(room.description, 'Стандартный номер')
        self.assertEqual(room.price_per_night, Decimal('3000.00'))
    
    def test_create_room_missing_description(self):
        """Тест создания номера без описания"""
        response = self.client.post('/rooms/create', {
            'price_per_night': '3000.00'
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_create_room_invalid_price(self):
        """Тест создания номера с невалидной ценой"""
        response = self.client.post('/rooms/create', {
            'description': 'Стандартный номер',
            'price_per_night': 'invalid_price'
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_delete_room_success(self):
        """Тест успешного удаления номера"""
        room = Room.objects.create(
            description="Номер для удаления",
            price_per_night=Decimal('2000.00')
        )
        
        response = self.client.post('/rooms/delete', {
            'room_id': room.id
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Room.objects.filter(id=room.id).exists())
    
    def test_delete_room_not_found(self):
        """Тест удаления несуществующего номера"""
        response = self.client.post('/rooms/delete', {
            'room_id': 999999
        })
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_list_rooms_default_sort(self):
        """Тест получения списка номеров с сортировкой по умолчанию"""
        room1 = Room.objects.create(
            description="Первый номер",
            price_per_night=Decimal('1000.00')
        )
        room2 = Room.objects.create(
            description="Второй номер",
            price_per_night=Decimal('2000.00')
        )
        
        response = self.client.get('/rooms/list')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        # По умолчанию сортировка по created_at asc
        self.assertEqual(data[0]['room_id'], room1.id)
        self.assertEqual(data[1]['room_id'], room2.id)
    
    def test_list_rooms_price_sort_desc(self):
        """Тест сортировки номеров по цене по убыванию"""
        room1 = Room.objects.create(
            description="Дешевый номер",
            price_per_night=Decimal('1000.00')
        )
        room2 = Room.objects.create(
            description="Дорогой номер",
            price_per_night=Decimal('5000.00')
        )
        
        response = self.client.get('/rooms/list?sort_by=price_per_night&order=desc')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]['room_id'], room2.id)  # Дорогой сначала
        self.assertEqual(data[1]['room_id'], room1.id)  # Дешевый потом


class BookingAPITest(TestCase):
    """Тесты API для бронирований"""
    
    def setUp(self):
        self.client = Client()
        self.room = Room.objects.create(
            description="Тестовый номер",
            price_per_night=Decimal('2000.00')
        )
        self.today = date.today()
        self.tomorrow = self.today + timedelta(days=1)
        self.day_after_tomorrow = self.today + timedelta(days=2)
    
    def test_create_booking_success(self):
        """Тест успешного создания бронирования"""
        response = self.client.post('/bookings/create', {
            'room_id': self.room.id,
            'date_start': self.tomorrow.strftime('%Y-%m-%d'),
            'date_end': self.day_after_tomorrow.strftime('%Y-%m-%d')
        })
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertIn('booking_id', data)
        
        booking = Booking.objects.get(id=data['booking_id'])
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.date_start, self.tomorrow)
    
    def test_create_booking_room_not_found(self):
        """Тест создания бронирования для несуществующего номера"""
        response = self.client.post('/bookings/create', {
            'room_id': 999999,
            'date_start': self.tomorrow.strftime('%Y-%m-%d'),
            'date_end': self.day_after_tomorrow.strftime('%Y-%m-%d')
        })
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_create_booking_invalid_dates(self):
        """Тест создания бронирования с некорректными датами"""
        response = self.client.post('/bookings/create', {
            'room_id': self.room.id,
            'date_start': self.day_after_tomorrow.strftime('%Y-%m-%d'),
            'date_end': self.tomorrow.strftime('%Y-%m-%d')
        })
        
        self.assertEqual(response.status_code, 400)
