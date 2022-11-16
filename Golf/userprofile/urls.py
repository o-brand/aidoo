from django.urls import path
from django.views.generic.base import TemplateView
from . import views

# Be aware that the url already includes "profile/"
urlpatterns = [
    path('<int:user_id>/', views.userdetail, name='userdetail'), # Details of a user
    path('me/', views.me, name='me'), # My profile
    path('genericprofile', views.generic_profile_call, name='genericprofile'), # Generic function to communicate with Django via JavaScript
]
