from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Room, Message
from Golf.settings import CHAT_MESSAGE_TTL


#Get actual user model
User = get_user_model()


def _query_rooms(me):
    """Query the rooms where one of the users is me."""
    rooms = Room.objects.filter(Q(user_1=me) | Q(user_2=me))

    # Change room object for the template
    rooms_changed = []
    for room in rooms:
        if room.user_2 == me:
            other = room.user_1
            room.user_1 = me
            room.user_2 = other
            room.me_started = False
        else:
            room.me_started = True

        rooms_changed.append(room)

    return rooms_changed


class RoomsView(ListView):
    """Displays a list to show the available rooms."""

    model = Room
    template_name = "chat/index.html"
    context_object_name = "rooms"

    def get_queryset(self):
        """Reads rooms from the database."""
        me = self.request.user
        return _query_rooms(me)


def refreshrooms_call(request):
    """Refresh rooms."""
    me = request.user
    return render(request, "htmx/rooms-list.html", {"rooms": _query_rooms(me)})

def searching_modal(request):
    """Searching modal."""
    return render(request, "chat/searching.html")

def searching_call(request):
    """Searching for users by username."""
    if request.method == "POST":
        me = request.user

        # Get the user ID or -1 if it is not found
        username = request.POST.get("username", -1)

        # If no username was given
        if username == -1:
            raise Http404()

        # Do not display anything if no text entered
        if len(username) == 0:
            return HttpResponse()

        users = User.objects.filter(username__icontains=username).exclude(pk=me.id)

        # Render the page
        return render(request, "htmx/searching.html", {"users": users})

    # If it is not POST
    raise Http404()

def room(request, user_id):
    """Displaying a room with the given user."""
    me = request.user

    # Check if the user ID is valid
    users = User.objects.filter(pk=user_id)
    user_id_exists = len(users) == 1
    if not user_id_exists:
        raise Http404()
    other_user = users[0]

    # Check if it is a room
    rooms = Room.objects.filter(Q(user_1=me, user_2=other_user) | Q(user_2=me, user_1=other_user))
    room_exists = len(rooms) == 1
    if not room_exists:
        # Create room
        rooms = dict()
        rooms["user_1"] = me
        rooms["user_2"] = other_user
        room = Room.objects.create(**rooms)
    else:
        room = rooms[0]

    if room.user_2 == me:
        room.user_1 = me
        room.user_2 = other_user

    messages = Message.objects.filter(room_id=room.room_id)
    return render(
        request,
        "chat/room.html",
        {
            "room": room,
            "user": other_user,
            "messages": messages,
            "in_room": True,
            "ttl": CHAT_MESSAGE_TTL,
        }
    )
