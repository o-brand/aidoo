import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Job, Comment


# Get actual user model.
User = get_user_model()


class CommentsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """Join room based on id in the URL."""
        self.room_id = self.scope['url_route']['kwargs']['job_id']
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
        content = data['content']
        commenter = data['commenter']
        commenter_id = data['commenter_id']
        commenter_url = data['commenter_url']

        # Save message
        date_time = await self.save_comment(commenter, self.room_id, content)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'comment',
                'content': content,
                'commenter': commenter,
                'commenter_id': commenter_id,
                'commenter_url': commenter_url,
                'date_time': date_time,
            }
        )

    async def comment(self, event):
        """Receive message from room group."""
        content = event['content']
        commenter = event['commenter']
        commenter_id = event['commenter_id']
        commenter_url = event['commenter_url']
        date_time = event['date_time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'content': content,
            'commenter': commenter,
            'commenter_id': commenter_id,
            'commenter_url': commenter_url,
            'me': self.me == commenter,
            'date_time': date_time,
        }))

    @sync_to_async
    def save_comment(self, username, room_id, content):
        """Save comment to the database."""
        commenter = User.objects.get(username=username)
        job = Job.objects.get(pk=room_id)

        # Create and save comment
        comment = dict()
        comment["job_id"] = job
        comment["commenter_id"] = commenter
        comment["content"] = content
        saved_comment = Comment.objects.create(**comment)

        to_tz = timezone.get_default_timezone()
        return saved_comment.post_time.astimezone(to_tz).strftime("%#d %b %Y, %I:%M %p")
