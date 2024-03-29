from datetime import datetime
from faker import Faker
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone


# Get actual user model.
User = get_user_model()


class LoginRequiredTestCase(TestCase):
    """This class can be used to test pages where login is required."""

    def setUp(self):
        """Creates a user and logs in."""
        credentials = {
            "username": "asd",
            "password": "asd123",
            "date_of_birth": datetime.now(),
            "profile_id": "media/profilepics/default",
        }
        self.user = User.objects.create_user(**credentials)
        self.client.post("/login", credentials, follow=True)


def create_date_string(difference):
    """Constructs a date string by substracting the difference from the actual
    year."""
    now = datetime.now()

    return f"{now.year - difference}-{now.month:02d}-{now.day:02d}"


def fake_time():
    """Returns a timezone aware time to prevent warnings."""
    fake = Faker()
    tz = timezone.get_current_timezone()
    return timezone.make_aware(fake.date_time(), tz, True)
