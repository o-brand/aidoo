from django.urls import path
from . import views


# Be aware that the url already includes "superadmin/"
urlpatterns = [
    # Homepage
    path("", views.ReportsView.as_view(), name="superadmin"),
    # Reporting a job, used by HTMX
    path("report", views.ReportFormView.as_view(), name="report"),
    # Conflict resolution call, used by HTMX
    path("conflict", views.conflict_call, name="conflict"),
]
