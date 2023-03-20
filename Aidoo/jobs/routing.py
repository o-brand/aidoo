from django.urls import path
from .consumers import CommentsConsumer

# URLs for websockets
websocket_urlpatterns = [
    path("ws/job/<int:job_id>", CommentsConsumer.as_asgi()),
]
