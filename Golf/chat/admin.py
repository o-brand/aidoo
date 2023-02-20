from django.contrib import admin
from .models import Room, Message


# Enable editing these models via /admin/.
admin.site.register(Room)
admin.site.register(Message)
