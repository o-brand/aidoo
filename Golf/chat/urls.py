from django.urls import path
from . import views


# Be aware that the url already includes "chat/"
urlpatterns = [
    # Homepage
    path("", views.RoomsView.as_view(), name="chat"),
    # Searching by username
    path("searching", views.searching, name="searching"),
    #
    path("search", views.searching_call, name="search"),
]
