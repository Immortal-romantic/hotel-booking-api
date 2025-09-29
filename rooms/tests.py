from django.test import TestCase

from rooms.models import Room


class RoomTests(TestCase):
    def test_create_room(self):
        r = Room.objects.create(description="Test room", price=10)
        self.assertIsNotNone(r.id)
        self.assertEqual(r.description, "Test room")
        self.assertEqual(str(r.price), "10")
