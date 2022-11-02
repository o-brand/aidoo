from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from django.views.generic.base import View

# Be aware that the url already includes "jobs/"
urlpatterns = [
    path('', views.JobsView.as_view(), name='home'), # Basic home with the jobs list
    path('post/', views.FormView.as_view(), name='post'), # Posting a job
    path('<int:job_id>/', views.detail, name='jobdetails'), # Details of a job
    path('sfl', views.sflcall, name='sfl'), # Save for later - Communication with Django via JavaScript
    path('generic', views.genericcall, name='generic'), # Generic function to communicate with Django via JavaScript
]
