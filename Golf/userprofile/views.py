from django.shortcuts import render
from django.contrib.auth.models import User
from jobs.models import Job, Bookmark, Application
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
        if request.POST['kind'] == 'exchange':
            jid = int(request.POST['jid']) # Job in question
            appid = int(request.POST['appid']) # ID of applicant
            release_points(id, jid, appid)
        else:
            user_id = request.POST["accept"][0]
            job_id = request.POST["accepted"]

            # we get row from the table with the job id
            job = Job.objects.get(pk=job_id)
            job.assigned = True
            job.save()

            # change status of applicants - only those status where "AP"
            set_rejected = Application.objects.filter(job_id=job_id, status="AP")
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
    saved = Bookmark.objects.filter(user_id=id)
    for job in saved:
        saved_jobs.append([job.job_id, job.saving_time])

    # Applied jobs
    applied_jobs = []
    applied = Application.objects.filter(user_id=id)
    for job in applied:
        applied_jobs.append([job.job_id, job.status])

    # Posted jobs
    posted_jobs = []
    posted = Job.objects.filter(poster_id=id)
    for job in posted:
         # Need to run the query, that is the reason for list.
        applicants = list(Application.objects.filter(job_id=job.job_id))
        posted_jobs.append([job, applicants])

    context = {
        'user': user_extended,
        'saved': saved_jobs,
        'applied': applied_jobs,
        'posted': posted_jobs,
    }
    return HttpResponse(template.render(context, request))

def release_points(rid, jid, appid): #rid = id of requester
    try:
        post = Job.objects.get(job_id=jid) # Job post
        if rid != post.poster_id.id:
            return HttpResponseNotFound()
        volunteer = User.objects.get(id=appid) # Applicant
        poster = User.objects.get(id=post.poster_id.id) # Job poster
        application = Application.objects.get(job_id=jid, user_id=appid) # Job process (?)
    except (User.DoesNotExist, Job.DoesNotExist, Application.DoesNotExist):
        return HttpResponseNotFound()
    else:
        poster.balance = poster.balance - post.points # Deduct points from job poster
        volunteer.balance = volunteer.balance + post.points # Pay points to volunteer
        post.completed = True # Set the post to completed
        application.status = "DN" # Set the job process to done

        poster.save()
        volunteer.save()
        post.save()
        application.save()