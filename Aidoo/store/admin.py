from django.contrib import admin
from .models import Item, Sale, Transfer, Moderation


# Enable editing these models via /admin/.
admin.site.register(Item)
admin.site.register(Sale)
admin.site.register(Transfer)
admin.site.register(Moderation)
