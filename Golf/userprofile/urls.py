from django.urls import path
from django.views.generic.base import TemplateView
from . import views

# Be aware that the url already includes "profile/"
urlpatterns = [
    path('<int:user_id>/', views.userdetail, name='userdetail'), # Details of a job
]
