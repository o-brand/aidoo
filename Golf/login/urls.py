from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import SignUpView, activateAccount, welcome


urlpatterns = [
    # Welcome page for the whole project
    path(route="",view=welcome,name="welcome"),

    # Login page
    path(
        route="login",
        view=auth_views.LoginView.as_view(template_name="login/login.html"),
        name="login",
    ),

    # Logout page
    path(
        route="logout",
        view=auth_views.LogoutView.as_view(),
        name="logout",
    ),

    # Registration page
    path(
        route="signup",
        view=SignUpView.as_view(),
        name="signup",
    ),

    # Password reset pages
    path(
        route="password_reset",
        view=auth_views.PasswordResetView.as_view(
            template_name="login/password_reset_form.html"
        ),
        name="password_reset_form",
    ),
    path(
        route="password_reset/sent",
        view=auth_views.PasswordResetDoneView.as_view(
            template_name="login/password_reset_sent.html"
        ),
        name="password_reset_sent",
    ),
    path(
        route="password_reset/<uidb64>/<token>",
        view=auth_views.PasswordResetConfirmView.as_view(
            template_name="login/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        route="password_reset/complete",
        view=auth_views.PasswordResetCompleteView.as_view(
            template_name="login/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    # Account activation pages
    path(
        route="activate/<uidb64>/<token>",
        view=activateAccount,
        name="activate",
    ),
    path(
        route="activation/success",
        view=TemplateView.as_view(template_name="login/activation_success.html"),
        name="activation_success",
    ),
    path(
        route="activation/failure",
        view=TemplateView.as_view(template_name="login/activation_failure.html"),
        name="activation_failure",
    ),
]
