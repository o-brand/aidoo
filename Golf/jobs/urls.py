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
     # Generic function to communicate with Django via JavaScript
    path("generic", views.generic_call, name="generic"),
    # Applying for a job, used by HTMX
    path("apply/<int:job_id>", views.apply_call, name="apply"),
    # Reporting a job, used by HTMX
    path("report/<int:job_id>", views.report_call, name="report"),
]
