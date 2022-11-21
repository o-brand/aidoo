from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import SignUpView, activateAccount

urlpatterns = [
    path('', TemplateView.as_view(template_name='welcome.html'), name='welcome'), # Welcome page for the whole project
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('privacy/', TemplateView.as_view(template_name='login/privacy.html'), name='privacy'), # Privacy policy
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='login/password_reset_form.html'), name='password_reset_form'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='login/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='login/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='login/password_reset_complete.html'), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activateAccount, name='activate'),
    path('confirm_email/',TemplateView.as_view(template_name='login/confirm_email.html'), name='confirm_email'),
    path('confirm_email/success/',TemplateView.as_view(template_name='login/confirm_email_success.html'), name='confirm_email_success'),
    path('confirm_email/failure/',TemplateView.as_view(template_name='login/confirm_email_failure.html'), name='confirm_email_failure'),
]
