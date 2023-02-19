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
    # Selecting an applicant, used by HTMX
    path("selectapplicant", views.selectapplicant_call, name="selectapplicant"),
    # Finishing a job, used by HTMX
    path("jobdone", views.jobdone_call, name="jobdone"),
    # User Settings
    path(
        route="settings",
        view=views.AccountSettingsView.as_view(),
        name="settings",
    ),
    # Notifications page
    path(
        route="notifications",
        view=views.NotificationsPageView.as_view(),
        name="notifications",
    ),
    # Marks a notification as seen, used by HTMX
    path("notification_seen", views.notification_seen, name="notification_seen"),
    
    # Notifications on navigation bar
    path(
        route="notification_nav",
        view=views.NotificationsNavView.as_view(),
        name="notification_nav",
    ),

]
