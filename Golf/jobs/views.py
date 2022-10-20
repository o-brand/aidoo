from django.shortcuts import render
from django.http import HttpResponse
from .models import JobPosting
from django.views.generic import ListView
from django.template import loader

def individualPost(request):
    recent_job = JobPosting.objects.get(pk=1)
    return HttpResponse(recent_job.job_title + ':' + recent_job.job_description)

def detail(request, job_id):
    template = loader.get_template('jobdetails.html')
    context = {
        'job': JobPosting.objects.get(pk=job_id),
    }
    return HttpResponse(template.render(context, request))

class JobsView(ListView):
   model               = JobPosting
   template_name       = 'home.html'
   context_object_name = 'jobs'

   def get_queryset(self):
        return JobPosting.objects.all()