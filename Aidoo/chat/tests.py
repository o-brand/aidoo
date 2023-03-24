import datetime
import json
import itertools
from asgiref.sync import sync_to_async
from channels.auth import AuthMiddlewareStack
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from faker import Faker
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from Aidoo.utils import LoginRequiredTestCase
from .views import _query_rooms
from .models import Room, Message
from .routing import websocket_urlpatterns as chat_url


# Get actual user model.
User = get_user_model()


class RoomQueryTestCase(LoginRequiredTestCase):

    def setUp(self):
        super().setUp()

        fake = Faker()

        # create 4 users in the database
        for _ in range(4):
            credentials = dict()
            credentials["username"] = fake.unique.name()
            credentials["password"] = "a"
            credentials["last_name"] = lambda: fake.last_name()
            credentials["first_name"] = lambda: fake.first_name()
            credentials["date_of_birth"] = datetime.datetime.now()
            credentials["profile_id"] = "media/profilepics/default"
            User.objects.create_user(**credentials)
            credentials.clear()

        pairings = [[1, 2], [3, 1]]
        for pair in pairings:
            room = dict()
            room["user_1"] = User(pk=pair[0])
            room["user_2"] = User(pk=pair[1])
            Room.objects.create(**room)

        for room in Room.objects.all():
            message = dict()
            message["room_id"] = room
            message["user_id"] = room.user_1
            message["content"] = "Hello"
            Message.objects.create(**message)

        for room in Room.objects.filter(user_2=self.user):
            message = dict()
            message["room_id"] = room
            message["user_id"] = room.user_1
            message["content"] = "Hello"
            Message.objects.create(**message)

        room = dict()
        room["user_1"] = User(pk=4)
        room["user_2"] = User(pk=1)
        Room.objects.create(**room)

    def test_query_rooms(self):
        queried_rooms = _query_rooms(User(pk=1))
        self.assertTrue(len(queried_rooms) != 0)


class RoomModelTestCase(LoginRequiredTestCase):
    """Tests for Room model."""

    def setUp(self):
        fake = Faker()

        # create 2 users in the database
        for _ in range(2):
            credentials = dict()
            credentials["username"] = fake.unique.name()
            credentials["password"] = "a"
            credentials["last_name"] = lambda: fake.last_name()
            credentials["first_name"] = lambda: fake.first_name()
            credentials["date_of_birth"] = datetime.datetime.now()
            credentials["profile_id"] = "media/profilepics/default"
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


class SearchingModalTestCase(LoginRequiredTestCase):
    """Tests for searching users. It is displayed in a modal."""

    def test_page(self):
        # test availability via URL
        response = self.client.get("/chat/searching-modal")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chat/searching.html")

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("chat-searching-modal"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chat/searching.html")


class SearchingCallButtonCase(LoginRequiredTestCase):
    """Tests for searching users by username, HTMX function."""

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
            credentials["profile_id"] = "media/profilepics/default"
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
        # test with an empty username
        response = self.client.post("/chat/searching", {})
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


class RoomCase(LoginRequiredTestCase):
    """Tests for room view."""

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
            credentials["profile_id"] = "media/profilepics/default"
            User.objects.create_user(**credentials)
            credentials.clear()

        room = dict()
        room["user_1"] = User(pk=1)
        room["user_2"] = User(pk=2)
        Room.objects.create(**room)

    def test_page(self):
        # test availability via URL
        response = self.client.get("/chat/room/2")
        self.assertEqual(response.status_code, 200)

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("chat-room", kwargs={"user_id": 2}))
        self.assertEqual(response.status_code, 200)

    def test_page_user_id_not_valid(self):
        # test with a wrong user id
        response = self.client.post("/chat/room/0")
        self.assertEqual(response.status_code, 404)

    def test_page_fine(self):
        response = self.client.post("/chat/room/2")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="chat/room.html")

    def test_page_start_chat_not_valid(self):
        # test with a wrong user id
        response = self.client.post("/chat/room", {"user_id": 0})
        self.assertEqual(response.status_code, 404)

    def test_page_post_chat_does_not_exist(self):
        # test for starting chat (start chat functionality)
        response = self.client.get("/chat/room/8")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Room.objects.all()), 2)

    def test_page_chat_not_me_created(self):
        # test for a room which was created by another user
        room = dict()
        room["user_1"] = User.objects.get(pk=5)
        room["user_2"] = self.user
        room = Room.objects.create(**room)

        response = self.client.get("/chat/room/5")
        self.assertEqual(response.status_code, 200)


@sync_to_async
def get_all_messages():
    """Reads all the messages. Used to test the consumer."""
    return list(Message.objects.all())

class ChatConsumerTestCase(LoginRequiredTestCase):

    def setUp(self):
        fake = Faker()

        # Login from super...
        super().setUp()

        # create 10 users in the database
        for i in range(2):
            if i == 0:
                username = "qwe"
            elif i == 1:
                username = "madeupuser"

            credentials = dict()
            credentials["username"] = username
            credentials["password"] = "a"
            credentials["last_name"] = lambda: fake.last_name()
            credentials["first_name"] = lambda: fake.first_name()
            credentials["date_of_birth"] = datetime.datetime.now()
            credentials["profile_id"] = "media/profilepics/default"
            User.objects.create_user(**credentials)
            credentials.clear()

        room = dict()
        room["user_1"] = User(pk=1)
        room["user_2"] = User(pk=2)
        Room.objects.create(**room)

    async def test_chat_message_function(self):
        # Connect
        application = AuthMiddlewareStack(URLRouter(chat_url))
        communicator = WebsocketCommunicator(application, "/ws/chat/1")
        await communicator.connect()

        # Send message
        await communicator.send_input({
            "type": "chat_message",
            "message": "Hi",
            "username": "madeupuser",
            "date_time": "2023-03-18",
        })

        # "Receive" message
        event = await communicator.receive_output()
        response = json.loads(event["text"])
        self.assertEqual(response["message"], "Hi")
        self.assertEqual(response["username"], "madeupuser")
        self.assertEqual(response["me"], False)
        self.assertEqual(response["date_time"], "2023-03-18")

        # Close
        await communicator.disconnect()

    async def test_receive_functions(self):
        # Connect
        application = AuthMiddlewareStack(URLRouter(chat_url))
        communicator = WebsocketCommunicator(application, "/ws/chat/1")
        await communicator.connect()

        # Send message
        await communicator.send_json_to({
            "message": "Hi",
            "username": "madeupuser",
        })
        event = await communicator.receive_from()
        response = json.loads(event)
        self.assertEqual(response["message"], "Hi")
        self.assertEqual(response["username"], "madeupuser")
        self.assertEqual(response["me"], False)

        # New message in the DB
        messages = await get_all_messages()
        self.assertEqual(len(messages), 1)

        # Close
        await communicator.disconnect()
