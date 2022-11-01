from django.shortcuts import render
from django.contrib.auth.models import User
from jobs.models import JobPosting, UserSaveForLater
from django.template import loader
from django.http import HttpResponse, HttpResponseNotFound

def userdetail(request, user_id):
    template = loader.get_template('userprofile/profile.html')

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponseNotFound()

    # Saved jobs
    saved_jobs = []
    saved = UserSaveForLater.objects.filter(user_id=user.id)
    for job in saved:
        saved_jobs.append([job.job_id, job.saving_time])

    context = {
        'user': user,
        'saved': saved_jobs,
    }
    return HttpResponse(template.render(context, request))
