from django.test import TestCase
from rooms.models import Room
from bookings.models import Booking
from datetime import date, timedelta

class BookingTests(TestCase):
    def setUp(self):
        self.room = Room.objects.create(description="Room for tests", price=20)

    def test_create_booking(self):
        # Используем относительные даты — всегда в будущем
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=2)
        b = Booking.objects.create(room=self.room, date_start=start, date_end=end)
        self.assertIsNotNone(b.id)
        self.assertEqual(b.room_id, self.room.id)

    def test_end_is_exclusive_allowed(self):
        # создаём бронь, затем другую, где date_start == existing.date_end (должно быть допустимо)
        start1 = date.today() + timedelta(days=5)
        end1 = start1 + timedelta(days=2)   # 5..7
        Booking.objects.create(room=self.room, date_start=start1, date_end=end1)

        # новая бронь начинается в end1 — это допустимо (end эксклюзивен)
        start2 = end1
        end2 = start2 + timedelta(days=1)
        b2 = Booking.objects.create(room=self.room, date_start=start2, date_end=end2)
        self.assertIsNotNone(b2.id)


