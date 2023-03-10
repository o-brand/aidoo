from django.urls import path
from . import views


# Be aware that the url already includes "vendor/".
urlpatterns = [
    # 
    path("<token>", views.redeem, name="redeem"),
]
