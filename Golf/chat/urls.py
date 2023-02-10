from django.urls import path
from . import views


# Be aware that the url already includes "chat/"
urlpatterns = [
    # Homepage
    path("", views.RoomsView.as_view(), name="chat"),
    # Starting a chat, used by HTMX
    path("startchat", views.startchat_call, name="chat-startchat"),
    # Searching by username, displayed in a modal
    path("searching", views.searching, name="chat-searching"),
    # Searching, used by HTMX
    path("search", views.searching_call, name="chat-search"),
]
