from django.shortcuts import render
from django.http import HttpResponse
from .models import JobPosting
from django.views.generic import ListView
from django.template import loader

import git
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("teamgolf.pythonanywhere.com/") 
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")


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
