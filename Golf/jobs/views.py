from django.shortcuts import render
from django.http import HttpResponse
from .models import JobPosting

def individualPost(request):
    recent_job = JobPosting.objects.get(pk=1)
    return HttpResponse(recent_job.job_title + ':' + recent_job.job_description)
