from django.shortcuts import render
from django.http import HttpResponse
from .models import JobPosting

def index(request):
    print("this is where the index goes")

def individualPost(request):
    recent_job = JobPosting.objects.get(id_exact = 1)
    return HttpResponse(recent_job.job_title + ':' + recent_job.job_description)


# Create your views here.
