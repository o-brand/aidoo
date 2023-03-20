from django.urls import path
from . import views


# Be aware that the url already includes "chat/"
urlpatterns = [
    # Homepage
    path("", views.RoomsView.as_view(), name="chat"),
    # Searching by username, displayed in a modal
    path("searching-modal", views.searching_modal, name="chat-searching-modal"),
    # Searching, used by HTMX
    path("searching", views.searching_call, name="chat-searching"),
    # A room with another user
    path("room/<int:user_id>", views.room, name="chat-room"),
]
