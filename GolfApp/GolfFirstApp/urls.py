from django.urls import path, include
from GolfFirstApp import views

urlpatterns = [
    path('GolfFirstApp/', views.GolfFirstApp, name='GolfFirstApp'),
]
