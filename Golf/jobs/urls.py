from django.urls import path
from django.views.generic.base import View
from django.views.generic.base import TemplateView
from . import views


# Be aware that the url already includes "jobs/".
urlpatterns = [
    # Basic home with the jobs list
    path("", views.JobsView.as_view(), name="home"),
    # Posting a job
    path("post", views.FormView.as_view(), name="post"),
    # Details of a job
    path("<int:job_id>", views.detail, name="jobdetails"),
     # Generic function to communicate with Django via JavaScript
    path("generic", views.generic_call, name="generic"),
]
