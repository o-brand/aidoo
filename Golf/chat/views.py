from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Room


#Get actual user model
User = get_user_model()


class RoomsView(ListView):
    """Displays a list to show the available rooms."""

    model = Room
    template_name = "chat/index.html"
    context_object_name = "rooms"

    def get_queryset(self):
        """Reads rooms from the database."""
        me = self.request.user
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


def startchat_call(request):
    """Start chat."""
    if request.method == "POST":
        # Get the user ID or -1 if it is not found
        user_id = request.POST.get("user_id", -1)
        me = request.user

        # Check if the user ID is valid
        users = User.objects.filter(pk=user_id)
        user_id_exists = len(users) == 1
        if not user_id_exists:
            raise Http404()
        invitee = users[0]

        # Create room
        room = dict()
        room["user_1"] = me
        room["user_2"] = invitee
        Room.objects.create(**room)

        return render(request, "htmx/chat_button.html")

    # If it is not POST
    raise Http404()


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

        # Get users
        users = User.objects.filter(username__icontains=username).exclude(pk=me.id)

        # Iterate over to display the adequate button
        users_with_chat_started = []
        for user in users:
            chat_started = len(Room.objects.filter(Q(user_1=me, user_2=user.id) | Q(user_2=me, user_1=user.id))) == 1
            users_with_chat_started.append([user, chat_started])

        # Render the page
        return render(request, "htmx/searching.html", {"users": users_with_chat_started})

    # If it is not POST
    raise Http404()

def room(request, user_id):

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
        return redirect('userdetails', user_id=user_id)
    room = rooms[0]



    return render(request, "chat/room.html")
