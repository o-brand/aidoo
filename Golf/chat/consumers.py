import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .models import Room, Message


# Get actual user model.
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """Join room based on id in the URL."""
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%d' % self.room_id
        self.me = self.scope['user'].username

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Leave room group."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Receive message from WebSocket."""
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # Save message
        await self.save_message(username, self.room_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        """Receive message from room group."""
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'me': self.me == username,
        }))

    @sync_to_async
    def save_message(self, username, room_id, content):
        """Save message to the database."""
        user = User.objects.get(username=username)
        room = Room.objects.get(room_id=room_id)

        # Create and save message
        message = dict()
        message["user_id"] = user
        message["room_id"] = room
        message["content"] = content
        Message.objects.create(**message)
