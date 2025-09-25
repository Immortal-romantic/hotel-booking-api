from django.test import TestCase
from rooms.models import Room  # явный импорт из app rooms

class RoomTests(TestCase):
    def test_create_room(self):
        r = Room.objects.create(description="Test room", price=10)
        self.assertIsNotNone(r.id)
        self.assertEqual(r.description, "Test room")
        # price — DecimalField, приводим к строке для стабильной проверки
        self.assertEqual(str(r.price), "10")
