from django.contrib import admin
from .models import Item, Sale


# Enable editing these models via /admin/.
admin.site.register(Item)
admin.site.register(Sale)