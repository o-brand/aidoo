import datetime
from faker import Faker
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from .models import Room


# Get actual user model.
User = get_user_model()


class RoomModelTestCase(TestCase):
    """Tests for Room model."""

    def setUp(self):
        fake = Faker()

        # create 2 users in the database
        for i in range(2):
            credentials = dict()
            credentials["username"] = fake.unique.name()
            credentials["password"] = "a"
            credentials["last_name"] = lambda: fake.last_name()
            credentials["first_name"] = lambda: fake.first_name()
            credentials["date_of_birth"] = datetime.datetime.now()
            User.objects.create_user(**credentials)
            credentials.clear()

    def test_unique_constraint(self):
        """Test if a non-unique user_1 and user_2 pair raises an error"""

        room = dict()
        room["user_1"] = User(pk=1)
        room["user_2"] = User(pk=2)
        Room.objects.create(**room)
        with self.assertRaises(IntegrityError):
            Room.objects.create(**room)
