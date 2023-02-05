from django.urls import path
from . import views


# Be aware that the url already includes "profile/"
urlpatterns = [
    # Details of a user
    path("<int:user_id>", views.userdetails, name="userdetails"),
    # My profile
    path("me", views.me, name="me"),
    # Withdrawing from a job, used by HTMX
    path("withdraw", views.withdraw_call, name="withdraw"),
    # Finishing a job, used by HTMX
    path("jobdone", views.jobdone_call, name="jobdone"),
]
