from django.shortcuts import render
from django.contrib.auth.models import User
from jobs.models import JobPosting, UserSaveForLater, JobProcess
from django.template import loader
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import get_user_model

User = get_user_model() # Get user model

# Public pofile page with just the basic information.
def userdetail(request, user_id):
    template = loader.get_template('userprofile/public.html')

    try:
        user_extended = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        'user': user_extended,
    }
    return HttpResponse(template.render(context, request))

# Private pofile page with more data.
def me(request):
    template = loader.get_template('userprofile/private.html')
    id = request.user.id

    # If the user accepted somebody
    if request.POST:
        user_id = request.POST["accept"][0]
        job_id = request.POST["accepted"]

        # we get row from the table with the job id
        job = JobPosting.objects.get(pk=job_id)
        job.assigned = True
        job.save()

        # change status of applicants - only those status where "AP"
        set_rejected = JobProcess.objects.filter(job_id=job_id, status="AP")
        for user in set_rejected:
            if str(user.user_id.id) != user_id:
                user.status = "RE"
                user.save()
            else:
                user.status = "AC"
                user.save()

    try:
        user_extended = User.objects.get(pk=id)
    except User.DoesNotExist:
        # This should not happen.
        return HttpResponseNotFound()

    # Saved jobs
    saved_jobs = []
    saved = UserSaveForLater.objects.filter(user_id=id)
    for job in saved:
        saved_jobs.append([job.job_id, job.saving_time])

    # Applied jobs
    applied_jobs = []
    applied = JobProcess.objects.filter(user_id=id)
    for job in applied:
        applied_jobs.append([job.job_id, job.status])

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
        'applied': applied_jobs,
        'posted': posted_jobs,
    }
    return HttpResponse(template.render(context, request))
