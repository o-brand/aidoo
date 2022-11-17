from django.urls import path
from . import views

# Be aware that the url already includes "profile/"
urlpatterns = [
    path('<int:user_id>/', views.userdetail, name='userdetail'), # Details of a user
    path('me/', views.me, name='me') # My profile
    ]
