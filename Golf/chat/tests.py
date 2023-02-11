import datetime
from faker import Faker
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from Golf.utils import LoginRequiredTestCase
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


class RoomsViewTestCase(LoginRequiredTestCase):
    """Tests for rooms page."""

    def setUp(self):
        # Login from super...
        super().setUp()

    def test_rooms(self):
        response = self.client.get("/chat/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chat/index.html")

    def test_rooms_available_by_name(self):
        response = self.client.get(reverse("chat"))
        self.assertEqual(response.status_code, 200)


class SearchingCallButtonCase(LoginRequiredTestCase):
    """Tests for searching users by username HTMX function."""

    def setUp(self):
        fake = Faker()

        # Login from super...
        super().setUp()

        # create 10 users in the database
        for i in range(10):
            if i == 0:
                username = "qwe"
            else:
                username = fake.unique.name()

            credentials = dict()
            credentials["username"] = username
            credentials["password"] = "a"
            credentials["last_name"] = lambda: fake.last_name()
            credentials["first_name"] = lambda: fake.first_name()
            credentials["date_of_birth"] = datetime.datetime.now()
            User.objects.create_user(**credentials)
            credentials.clear()

    def test_page(self):
        # test availability via URL
        response = self.client.get("/chat/searching")
        self.assertEqual(response.status_code, 404)

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("chat-searching"))
        self.assertEqual(response.status_code, 404)

    def test_page_post_no_username(self):
        # test without sending a username
        response = self.client.post("/chat/searching")
        self.assertEqual(response.status_code, 404)

    def test_page_post_username_empty(self):
        # test with an empty username
        response = self.client.post("/chat/searching", {"username": ""})
        self.assertEqual(response.status_code, 200) # Empty response

    def test_page_post_username(self):
        # test works
        response = self.client.post("/chat/searching", {"username": "qwe"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="htmx/searching.html")
