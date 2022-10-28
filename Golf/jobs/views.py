from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .models import JobPosting
from django.views.generic import ListView
from django.views import View
from django.template import loader
from .forms import JobForm
import time

def detail(request, job_id):
    template = loader.get_template('jobdetails.html')

    try:
        job = JobPosting.objects.get(pk=job_id)
    except JobPosting.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        'job': job,
    }
    return HttpResponse(template.render(context, request))

class JobsView(ListView):
   model               = JobPosting
   template_name       = 'home.html'
   context_object_name = 'jobs'

   def get_queryset(self):
        return JobPosting.objects.all()

def testcall(request):
    print("HI", request.POST['text'])
    time.sleep(3) # Sleep...
    return HttpResponse("ok")

class FormView(View):
    form_class = JobForm
    template_name = "postjob.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/jobs/")

        return render(request, FormView.template_name, {'form': form})
