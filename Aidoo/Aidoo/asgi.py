"""ASGI config for Aidoo project."""

import os
from django.core.asgi import get_asgi_application


# Start the app
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Aidoo.settings")
asgi_app = get_asgi_application()


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns as chat_url
from jobs.routing import websocket_urlpatterns as jobs_url


# Register the app
application = ProtocolTypeRouter({
    "http": asgi_app,
    "websocket": AuthMiddlewareStack(URLRouter(chat_url + jobs_url))
})
