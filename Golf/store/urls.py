from django.urls import path
from . import views
from store.views import send_QRcode
from django.urls import re_path


# Be aware that the url already includes "store/"
urlpatterns = [
    # Homepage
    path("", views.home, name="store"),
    # Buy an item from the store, uses HTMX
    path("buyitem", views.buyitem_call, name="buyitem"),
    # Transfer form displayed in modal, uses HTMX
    path("transfer", views.TransferView.as_view(), name="transfer"),
]
