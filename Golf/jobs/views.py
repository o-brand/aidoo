from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .models import User, JobPosting, UserSaveForLater
from django.views.generic import ListView
from django.views import View
from django.template import loader
from .forms import JobForm
from django.utils import timezone
import time
import datetime

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

def sflcall(request, **kwargs):
    tz = timezone.get_current_timezone()
    timzone_datetime = timezone.make_aware(datetime.datetime.now(tz=None), tz, True)
    new_sfljob = UserSaveForLater(
        user_id=User.objects.get(pk=int(request.POST['uid'])),
        job_id=JobPosting.objects.get(pk=int(request.POST['jid'])),
        saving_time=timzone_datetime)
    new_sfljob.save()
    return HttpResponse("ok")

function_dict = {'sfl' : sflcall,}
def genericcall(request):
    function_dict[request.POST['func']]() #how to pass keyword args?
    return HttpResponse("ok")


class FormView(View):
    form_class = JobForm
    template_name = "postjob.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'poster_id': request.user.id})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/jobs/")

        return render(request, FormView.template_name, {'form': form, 'poster_id': request.user.id})
