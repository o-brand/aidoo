from django.urls import path
from django.views.generic.base import TemplateView
from . import views

# Be aware that the url already includes "jobs/"
urlpatterns = [
    path('', views.JobsView.as_view(), name='home'), # Basic home with the jobs list
    path('post/', TemplateView.as_view(template_name='postjob.html'), name='post'), # Posting a job
    path('<int:job_id>/', views.detail, name='jobdetails'), # Details of a job
]
