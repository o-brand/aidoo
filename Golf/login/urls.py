from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import SignUpView

urlpatterns = [
    path('', TemplateView.as_view(template_name='welcome.html'), name='welcome'), # Welcome page for the whole project
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("signup/", SignUpView.as_view(), name="signup"),
]
