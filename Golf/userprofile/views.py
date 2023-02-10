from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from jobs.models import Job, Bookmark, Application
from django.template.loader import render_to_string
from chat.models import Room


# Get actual user model.
User = get_user_model()


def userdetails(request, user_id):
    """Public pofile page with just the basic information."""
    requester = request.user #The user who is currently signed in

    try:
        user_extended = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("User does not exist.")

    posted_active = Job.objects.filter(poster_id=user_id, completed=False)
    posted_inactive = Job.objects.filter(Q(completed=True) | Q(hidden=True), poster_id=user_id)
    chat_started = len(Room.objects.filter(Q(user_1=requester, user_2=user_id) | Q(user_2=requester, user_1=user_id))) == 1
    context = {
        "user": requester,
        "viewed_user": user_extended,
        "posted_active": posted_active,
        "posted_inactive": posted_inactive,
        "chat_started": chat_started,
    }
    return render(request, "userprofile/public.html", context)


def startchat_call(request):
    """Start chat."""
    if request.method == "POST":
        # Get the user ID or -1 if it is not found
        user_id = request.POST.get("user_id", -1)
        user = request.user

        # Check if the user ID is valid
        users = User.objects.filter(pk=user_id)
        user_id_exists = len(users) == 1
        if not user_id_exists:
            raise Http404()
        other_user = users[0]

        # Create room
        room = dict()
        room["user_1"] = user
        room["user_2"] = other_user
        Room.objects.create(**room)

        return render(request, "htmx/chat_button.html")

    # If it is not POST
    raise Http404()


def me(request):
    """Private pofile page with more data."""
    actual_user_id = request.user.id

    try:
        user_extended = User.objects.get(pk=actual_user_id)
    except User.DoesNotExist:
        # This should not happen.
        raise Http404("User does not exist.")

    # Saved jobs
    saved_jobs = []

    saved = Bookmark.objects.filter(user_id=actual_user_id)

    for job in saved:
        saved_jobs.append([job.job_id, job.saving_time])

    # Applied jobs
    applied_jobs = []

    applied = Application.objects.filter(applicant_id=actual_user_id)

    for job in applied:
        applied_jobs.append([job.job_id, job.status])

    # Posted jobs
    posted_jobs = []

    posted = Job.objects.filter(poster_id=actual_user_id)

    for job in posted:
         # Need to run the query, that is the reason for list.
        applicants = list(Application.objects.filter(job_id=job.job_id))
        posted_jobs.append([job, applicants])

    context = {
        "user": user_extended,
        "saved": saved_jobs,
        "applied": applied_jobs,
        "posted": posted_jobs,
    }
    return render(request, "userprofile/private.html", context)


def withdraw_call(request):
    """Withdraw from a job."""
    if request.method == "POST":
        # Get the job ID or -1 if it is not found
        job_id = request.POST.get("job_id", -1)
        user = request.user

        # Check if the job ID is valid
        jobs = Job.objects.filter(pk=job_id)
        job_id_exists = len(jobs) == 1
        if not job_id_exists:
            raise Http404()

        # Check if there is an application
        applications = Application.objects.filter(applicant_id=user.id, job_id=job_id)
        application_exists = len(applications) == 1
        if not application_exists:
            raise Http404()

        # Withdraw
        application = applications[0]
        application.status = "WD"
        application.save()

        return render(
            request, "htmx/job-applied.html", {"job": jobs[0], "status": application.status}
        )

    # If it is not POST
    raise Http404()

def selectapplicant_call(request):
    """Select an applicant for a job."""
    if request.method == "POST":
        # Get the job ID or -1 if it is not found
        job_id = request.POST.get("job_id", -1)
        applicant_id = request.POST.get("accept", [-1])

        # Check if the job ID is valid
        jobs = Job.objects.filter(pk=job_id)
        job_id_exists = len(jobs) == 1
        if not job_id_exists:
            raise Http404()
        job = jobs[0]

        # Check if there is at least one application
        applications = Application.objects.filter(job_id=job_id, status="AP")
        no_application = len(applications) == 0
        if no_application:
            raise Http404()

        # Assign the job
        job.assigned = True
        job.save()

        # change status of applicants - only those status where "AP"
        for user in applications:
            if str(user.applicant_id.id) != applicant_id:
                # send an email to the rejected applicant
                message = render_to_string(
                    "emails/application_rejection.html",
                    {
                        "user": user.applicant_id.username,
                        "job_title": job.job_title,
                        "poster": job.poster_id.username,
                    },
                )
                send_mail(
                    'Sorry!',
                    message,
                    None,
                    [user.applicant_id.email],
                )

                user.status = "RE"
                user.save()
            else:
                # send an email to the accepted applicant
                message = render_to_string(
                    "emails/application_acceptance.html",
                    {
                        "user": user.applicant_id.username,
                        "job_title": job.job_title,
                        "poster": job.poster_id.username,
                    },
                )
                send_mail(
                    'Congratulations!',
                    message,
                    None,
                    [user.applicant_id.email],
                )

                user.status = "AC"
                user.save()
        return render(
            request, "htmx/job-applicants.html", {"job": job, "applicants": applications}
        )

    # If it is not POST
    raise Http404()

def jobdone_call(request):
    """Finish a job."""
    if request.method == "POST":
        # Get the job ID or -1 if it is not found
        job_id = request.POST.get("job_id", -1)
        user = request.user

        # Check if the job ID is valid
        jobs = Job.objects.filter(pk=job_id)
        job_id_exists = len(jobs) == 1
        if not job_id_exists:
            raise Http404()
        job = jobs[0]

        # Check if there is an application
        applications = Application.objects.filter(job_id=job_id, status="AC")
        application_exists = len(applications) == 1
        if not application_exists:
            raise Http404()
        application = applications[0]

        # Get volunteer, poster
        volunteer = User.objects.get(pk=application.applicant_id.id)
        poster = User.objects.get(id=user.id) # Job poster

        # Work...
        poster.balance = poster.balance - job.points # Deduct points from job poster
        volunteer.balance = volunteer.balance + job.points # Pay points to volunteer
        job.completed = True # Set the post to completed
        application.status = "DN" # Set the job process to done
        application.time_of_final_status = timezone.now() # Set the time of the final status

        poster.save()
        volunteer.save()
        job.save()
        application.save()

        applicants = list(Application.objects.filter(job_id=job.job_id))

        return render(
            request, "htmx/job-applicants.html", {"job": job, "applicants": applicants}
        )

    # If it is not POST
    raise Http404()
