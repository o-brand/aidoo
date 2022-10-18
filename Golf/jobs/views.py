from django.shortcuts import render
from django.http import HttpResponse
from .models import JobPosting
from django.views.generic import ListView

def individualPost(request):
    recent_job = JobPosting.objects.get(pk=1)
    return HttpResponse(recent_job.job_title + ':' + recent_job.job_description)

class JobsView(ListView):
   model               = JobPosting
   template_name       = 'home.html'
   context_object_name = 'jobs'

   def get_queryset(self):
        return JobPosting.objects.all()
