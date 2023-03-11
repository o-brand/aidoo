from django.urls import path
from . import views


# Be aware that the url already includes "vendor/".
urlpatterns = [
    # Redeeming a bought item, used by HTMX
    path("redeem", views.redeem_call, name="redeem-item"),
    # Used to display a bought item to redeem 
    path("<token>", views.redeem, name="redeem"),
]
