from django.shortcuts import render
from django.contrib.auth.models import User
from jobs.models import JobPosting, UserSaveForLater, UserExtended, JobProcess
from django.template import loader
from django.http import HttpResponse, HttpResponseNotFound

# Public pofile page with just the basic information.
def userdetail(request, user_id):
    template = loader.get_template('userprofile/public.html')

    try:
        user_extended = UserExtended.objects.get(pk=user_id)
    except UserExtended.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        'user': user_extended,
    }
    return HttpResponse(template.render(context, request))

# Private pofile page with more data.
def me(request):
    template = loader.get_template('userprofile/private.html')
    id = request.user.id

    try:
        user_extended = UserExtended.objects.get(pk=id)
    except UserExtended.DoesNotExist:
        # This should not happen.
        return HttpResponseNotFound()

    # Saved jobs
    saved_jobs = []
    saved = UserSaveForLater.objects.filter(user_id=id)
    for job in saved:
        saved_jobs.append([job.job_id, job.saving_time])

    # Posted jobs
    posted_jobs = []
    posted = JobPosting.objects.filter(poster_id=id)
    for job in posted:
         # Need to run the query, that is the reason for list.
        applicants = list(JobProcess.objects.filter(job_id=job.job_id))
        posted_jobs.append([job, applicants])

    context = {
        'user': user_extended,
        'saved': saved_jobs,
        'posted': posted_jobs,
    }
    return HttpResponse(template.render(context, request))
