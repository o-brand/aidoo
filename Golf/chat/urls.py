from django.urls import path
from . import views

# Be aware that the url already includes "chat/"
urlpatterns = [
    path("", views.home, name="chat"),

]
