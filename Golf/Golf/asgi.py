"""
ASGI config for Golf project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application


# Start the app
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Golf.settings")
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
