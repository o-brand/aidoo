from django.urls import path
from django.views.generic.base import TemplateView
from . import views

# Be aware that the url already includes "jobs/"
urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'), # Basic home
    path('jobs/',views.individualPost, name='jobs'),
    path('post/', TemplateView.as_view(template_name='postjob.html'), name='post'), # Posting a job
]
