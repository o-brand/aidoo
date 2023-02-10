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
        return Room.objects.filter(Q(user_1=me) | Q(user_2=me))

def searching(request):
    return render(request, "chat/searching.html")

def searching_call(request):
    if request.method == "POST":
        # Get the user ID or -1 if it is not found
        user_name = request.POST.get("user_name", -1)
        print(user_name)
        me = request.user
        if len(user_name) == 0:
            return HttpResponse()
        # Check if the user ID is valid
        users = User.objects.filter(username__icontains=user_name).exclude(pk=me.id)

        users_with_chat_status = []
        for user in users:
            chat_started = len(Room.objects.filter(Q(user_1=me, user_2=user.id) | Q(user_2=me, user_1=user.id))) == 1
            users_with_chat_status.append([user, chat_started])

        return render(request, "htmx/searching.html", {"users": users_with_chat_status})
    # If it is not POST
    raise Http404()
