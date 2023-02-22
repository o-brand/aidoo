from random import choice
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from django.template.loader import render_to_string
from django.views import View
from django.core.paginator import Paginator
from jobs.models import Job, Bookmark, Application
from .models import Notification
from chat.models import Room
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse


# Get actual user model.
User = get_user_model()


def userdetails(request, user_id):
    """Public pofile page with just the basic information."""
    me = request.user # The user who is currently signed in

    # Check if the user ID is valid
    users = User.objects.filter(pk=user_id)
    user_id_exists = len(users) == 1
    if not user_id_exists:
        raise Http404()
    user = users[0]

    posted_active = Job.objects.filter(poster_id=user.id, completed=False)
    posted_inactive = Job.objects.filter(Q(completed=True) | Q(hidden=True), poster_id=user.id)
    chat_started = (
        len(
            Room.objects.filter(
                Q(user_1=me, user_2=user.id) | Q(user_2=me, user_1=user.id)
            )
        ) == 1
    )
    context = {
        "me": me,
        "user": user,
        "posted_active": posted_active,
        "posted_inactive": posted_inactive,
        "chat_started": chat_started,
    }
    return render(request, "userprofile/public.html", context)


def me(request):
    """Private pofile page with more data."""
    actual_user_id = request.user.id

    # Check if the user ID is valid
    users = User.objects.filter(pk=actual_user_id)
    user_id_exists = len(users) == 1
    if not user_id_exists:
        raise Http404()
    me = users[0]

    # Saved jobs
    saved_jobs = []

    saved = Bookmark.objects.filter(user_id=actual_user_id
        ).order_by("saving_time")

    for job in saved:
        saved_jobs.append([job.job_id, job.saving_time])

    bookmark_paginator = Paginator(saved, 2)
    bookmark_page = request.GET.get("bpage")
    bookmarks = bookmark_paginator.get_page(bookmark_page)

    # Applied jobs
    applied_jobs = []

    applied = Application.objects.filter(applicant_id=actual_user_id)

    for job in applied:
        applied_jobs.append([job.job_id, job.status])

    application_paginator = Paginator(applied_jobs, 2)
    application_page = request.GET.get("apage")
    applications = application_paginator.get_page(application_page)

    # Posted jobs
    posted_jobs = []

    posted = Job.objects.filter(poster_id=actual_user_id)

    for job in posted:
         # Need to run the query, that is the reason for list.
        applicants = list(Application.objects.filter(job_id=job.job_id))
        posted_jobs.append([job, applicants])

    posts_paginator = Paginator(posted_jobs, 2)
    posts_page = request.GET.get("ppage")
    posts = posts_paginator.get_page(posts_page)

    context = {
        "me": me,
        "bookmarks": bookmarks,
        "posts": posts,
        "applications": applications,
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

        # Select applicant randomly
        selected_application = choice(applications)

        # Change status of applicants - only those status where "AP"
        for user in applications:
            if user.applicant_id.id != selected_application.applicant_id.id:
                # Check if user accepts email notifications before email send
                if user.applicant_id.opt_in_emails_application:
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
                        html_message=message,
                    )

                # Checks if the user accepts on site notifications
                # If true, create a new notification in the database
                if user.applicant_id.opt_in_site_application == True:
                    Notification.objects.create(
                        user_id = user.applicant_id, 
                        content = "You've been rejected from the job: " + str(job.job_title), 
                        link = "/jobs/" + str(job.job_id)
                        )

                user.status = "RE"
                user.save()
            else:
                # Checks if user accepts email notifications before email send
                if user.applicant_id.opt_in_emails_application:
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
                        html_message=message,
                    )

                # Checks if the user accepts on site notifications
                # If true, create a new notification in the database
                if user.applicant_id.opt_in_site_application == True:
                    Notification.objects.create(
                        user_id = user.applicant_id, 
                        content = "You've been accepted for the job: " + str(job.job_title), 
                        link = "/jobs/" + str(job.job_id)
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
        poster.frozen_balance = poster.frozen_balance - job.points # Deduct points from job poster
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


class AccountSettingsView(View):
    """It is used to render the account settings page."""

    template_name = "userprofile/usersettings.html"

    # Renders the form at the first time
    def get(self, request, *args, **kwargs):
        me = request.user
        return render(request, self.template_name, {"me":me})

    # Processes the form after submit
    def post(self, request, *args, **kwargs):
        #returns an empty list if button is unchecked otherwise returns ['on']
        button_check_1 = request.POST.getlist('opt_in_1')
        button_check_2 = request.POST.getlist('opt_in_2')
        button_check_3 = request.POST.getlist('opt_in_3')

        me = request.user

        # If checkbox state doesn't match email preference on submit
        # then change the email preference
        if me.opt_in_emails_application == True and button_check_1 == []:
            me.opt_in_emails_application = False
        elif me.opt_in_emails_application == False and button_check_1 == ['on']:
            me.opt_in_emails_application = True
        
        # If checkbox state doesn't match email preference on submit
        # then change the on site preference
        if me.opt_in_site_application == True and button_check_2 == []:
            me.opt_in_site_application = False
        elif me.opt_in_site_application == False and button_check_2 == ['on']:
            me.opt_in_site_application = True
        
        # If checkbox state doesn't match email preference on submit
        # then change the email preference
        if me.opt_in_site_applicant == True and button_check_3 == []:
            me.opt_in_site_applicant = False
        elif me.opt_in_site_applicant == False and button_check_3 == ['on']:
            me.opt_in_site_applicant = True
        
        me.save()

        # Render the form again
        return render(request, self.template_name, {"me":me})

class NotificationsPageView(ListView):
    """It is used to render the notifications page."""

    model = Notification
    context_object_name = "notifs"
    template_name = "userprofile/notifications.html"
    
    # Returns a query of all notifications for the logged in user
    def get_queryset(self):
        me = self.request.user
        return Notification.objects.filter(user_id=me.id)
    
    # Returns a count of all notifications for the logged in user
    def notif_count(self):
        """Returns the number of notifications."""
        return self.get_queryset().count()
    
    # Returns a count of all unseen notifications
    def notif_seen_count(self):
        """Returns the number of unseen notifications."""
        me = self.request.user
        return self.get_queryset().filter(seen=False).count()

    # Creates the context to send to the template
    def get_context_data(self, **kwargs):
        """Adds data to the template."""
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context["notif_count"] = self.notif_count()

        context["notif_seen_count"] = self.notif_seen_count()

        return context
    
def notification_seen(request):
    """Marks a notification as seen when clicked by the user."""
    if request.method == "POST":

        # Obtains the id for the notification through htmx include
        n_id = request.POST['id']

        # Obtain the instance in the database for the clicked notification
        notification = Notification.objects.filter(notification_id=n_id)[0]

        notification.seen = True
        notification.save()

        # Redirect the user to the link saved in the notification
        response = HttpResponse()
        response["HX-Redirect"] = notification.link
        return response
