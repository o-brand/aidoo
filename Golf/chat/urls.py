from django.urls import path
from . import views


# Be aware that the url already includes "chat/"
urlpatterns = [
    # Homepage
    path("", views.home, name="chat"),
]