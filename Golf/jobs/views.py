from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .models import JobPosting, UserSaveForLater, JobProcess
from django.views.generic import ListView
from django.views import View
from django.template import loader
from .forms import JobForm
from django.utils import timezone
import time
import datetime
import json
from django.contrib.auth import get_user_model

User = get_user_model() # Get user model

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
        filter_val = self.request.GET.get('job_title__icontains', '')

        return JobPosting.objects.filter(hidden=False,job_title__icontains=filter_val)

   def job_count(self): 
        filter_val = self.request.GET.get('job_title__icontains', '')
        available = JobPosting.objects.filter(hidden=False,job_title__icontains=filter_val)
        i = 0
        for _ in available:
            i += 1
        return i

   def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the saved for later jobs
        context['saveforlater'] = UserSaveForLater.objects.filter(user_id=self.request.user.id)
        return context

# Executed when saveForLater is run on the frontend (i.e. save for later button pressed)
def sfl_call(request):
    uid = int(request.POST['uid'])
    jid = int(request.POST['jid'])
    try:
        u = UserSaveForLater.objects.get(user_id=uid, job_id=jid)
    except UserSaveForLater.DoesNotExist:
        tz = timezone.get_current_timezone()
        timzone_datetime = timezone.make_aware(datetime.datetime.now(tz=None), tz, True)
        new_sfljob = UserSaveForLater( # Make new UserSaveForLater record
            user_id=User.objects.get(pk=int(request.POST['uid'])),
            job_id=JobPosting.objects.get(pk=int(request.POST['jid'])),
            saving_time=timzone_datetime)
        new_sfljob.save() # Save new UserSaveForLater record in database table
    else:
        u.delete()
    finally:
        return HttpResponse("ok")

def apply_call(request):
    uid = int(request.POST['uid'])
    jid = int(request.POST['jid'])
    try: 
        u = JobProcess.objects.get(user_id=uid, job_id=jid)
    except JobProcess.DoesNotExist:
        new_apply = JobProcess(
            user_id = User.objects.get(pk = int(request.POST['uid'])),
            job_id = JobPosting.objects.get(pk=int(request.POST['jid'])),
        )
        new_apply.save()
    finally:
        return HttpResponse("ok")

def report_call(request):
    return HttpResponse("ok")

def indb_sfl_call(request):
    uid = int(request.POST['uid'])
    sfls = UserSaveForLater.objects.filter(user_id=uid)
    result = []
    for i in sfls:
        result.append(f"{i.job_id.job_id}")
    result_json = json.dumps(result)
    return HttpResponse(result_json)

def indb_app_call(request):
    uid = int(request.POST['uid'])
    jps = JobProcess.objects.filter(user_id=uid)
    result = []
    for i in jps:
        result.append(f"{i.job_id.job_id}")
    result_json = json.dumps(result)
    return HttpResponse(result_json)


# A dictionary of functions we define to run through genericcall (so we can use only one url)

#this is the dictionary, used in home.html: function sendid(uid...) .data {func: "sfl"}
function_dict = {'sfl': sfl_call, #save for later/unsave toggle function
                'app': apply_call,
                'report': report_call, 
                'indb_sfl': indb_sfl_call,
                'indb_app' : indb_app_call}

# Runs a function in our dictionary, as specified by the frontend function calling it
def generic_call(request):
    return function_dict[request.POST['func']](request)
    # Make sure that your functions return HttpResponse object or similar

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
