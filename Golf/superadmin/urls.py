from django.urls import path
from . import views


# Be aware that the url already includes "superadmin/"
urlpatterns = [
    # Homepage
    path("", views.home, name="superadmin"),
    # Reporting a job, used by HTMX
    path("report", views.ReportFormView.as_view(), name="report"),
]
