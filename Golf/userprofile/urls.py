from django.urls import path
from django.views.generic import TemplateView
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
    path(
        "notification_seen",
        views.notification_seen,
        name="notification_seen"),
    # Private profile card
    path("privatecard", views.my_details, name="privatecard"),
    # Profile editing form
    path("editprofile", views.ProfileEditView.as_view(), name="editprofile"),
    # Private profile commitments
    path("commitments", views.commitments, name="commitments"),
    # Private profile applications
    path("applications", views.applications, name="applications"),
    # Private profile posts
    path("posts", views.posts, name="posts"),
    # Private profile posts
    path("bookmarks", views.bookmarks, name="bookmarks"),
    # Balance badge
    path(
        "balance",
        TemplateView.as_view(template_name="userprofile/balance.html"),
        name="balance"),
]
