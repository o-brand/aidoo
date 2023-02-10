from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Room


class RoomsView(ListView):
    """Displays a list to show the available rooms."""

    model = Room
    template_name = "chat/index.html"
    context_object_name = "rooms"

    def get_queryset(self):
        """Reads rooms from the database."""
        return Room.objects.all() # TODO
