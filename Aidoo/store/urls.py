from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView
from . import views


# Be aware that the url already includes "store/"
urlpatterns = [
    # Homepage
    path("", views.home, name="store"),
    # Buy an item from the store, used by HTMX
    path("buyitem", views.buyitem_call, name="buyitem"),
    # Transfer form displayed in modal, used by HTMX
    path("transfer", views.TransferView.as_view(), name="transfer"),
    # Item card
    path(
        "item",
        TemplateView.as_view(template_name="store/item-card.html"),
        name="item"),
    # All item cards
    path(
        "items",
        TemplateView.as_view(template_name="store/items.html"),
        name="items"),
]
