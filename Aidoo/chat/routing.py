from django.urls import path
from .consumers import ChatConsumer

# URLs for websockets
websocket_urlpatterns = [
    path("ws/chat/<int:room_id>", ChatConsumer.as_asgi()),
]
