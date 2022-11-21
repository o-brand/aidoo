from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from userprofile.models import User


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
        }
        self.user = User.objects.create_user(**credentials)
        self.client.post("/login", credentials, follow=True)


def create_date_string(difference):
    """Constructs a date string by substracting the difference from the actual
    year."""
    now = datetime.now()

    return f"{now.year - difference}-{now.month:02d}-{now.day:02d}"
