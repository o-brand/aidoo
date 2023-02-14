from django.urls import path
from . import views


# Be aware that the url already includes "jobs/".
urlpatterns = [
    # Basic home with the jobs list
    path("", views.JobsView.as_view(), name="home"),
    # Posting a job
    path("post", views.FormView.as_view(), name="post"),
    # Details of a job
    path("<int:job_id>", views.details, name="jobdetails"),
    # Applying for a job, used by HTMX
    path("apply", views.apply_call, name="apply"),
    # Bookmarking a job, used by HTMX
    path("bookmark", views.bookmark_call, name="bookmark"),
]
