from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView
from django.views import View
from userprofile.models import Notification
from .models import Job, Bookmark, Application, Comment
from .forms import JobForm


# Get actual user model.
User = get_user_model()


def details(request, job_id):
    """Shows the details of a job."""

    # Read the job from the database
    try:
        job = Job.objects.get(pk=job_id, hidden=False)
    except Job.DoesNotExist:
        raise Http404()

    # Comments for the job
    comments = Comment.objects.filter(job_id=job.job_id)

    # Obtains the status of the logged in user for the viewed job
    try:
        status = Application.objects.filter(
            applicant_id=request.user.id, job_id=job.job_id
        )[0].status
    except:
        status = "NA"

    # Filter the bookmark state for the current user
    bookmarks = Bookmark.objects.filter(user_id=request.user.id, job_id=job.job_id)
    if len(bookmarks) == 1:
        bookmark = True
    else:
        bookmark = False

    # Give the found job to the template
    context = {
        "job": job,
        "comments": comments,
        "status": status,
        "bookmark": bookmark,
    }

    # Render the page
    return render(request, "jobdetails.html", context)


class FormView(View):
    """Displays a form for posting a job."""

    form_class = JobForm
    template_name = "postjob.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {"form": form, "poster_id": request.user.id},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # Recalculate points (because of security - the user could change the calculated value)
            duration_hours = form.cleaned_data["duration_hours"]
            duration_half_hours = form.cleaned_data["duration_half_hours"]
            post = form.save(commit=False)
            post.points = (duration_hours * 12) + int(duration_half_hours / 30) * 6

            # Check if the user has enough points
            me = request.user
            if me.balance < post.points:
                form.add_error(None, "You do not have sufficient funds")
                return render(
                    request,
                    self.template_name,
                    {"form": form, "poster_id": request.user.id},
                )

            # Save the job
            post.save()

            # Freeze points
            me.frozen_balance = me.frozen_balance + post.points
            me.balance = me.balance - post.points
            me.save()

            # No content
            return HttpResponse(
                status=204, headers={"HX-Trigger": "new_post"}
            )

        return render(
            request,
            self.template_name,
            {"form": form, "poster_id": request.user.id},
        )


class JobsView(ListView):
    """Displays a list to show the available jobs."""

    model = Job
    template_name = "home.html"
    context_object_name = "jobs"

    def get_queryset(self):
        """Reads jobs from the database."""
        filter_val = self.request.GET.get("search", "")
        return Job.objects.filter(
            Q(job_title__icontains=filter_val)
            | Q(job_description__icontains=filter_val)
            | Q(location__icontains=filter_val),
            hidden=False,
            assigned=False,
        ).exclude(poster_id_id=self.request.user.id)

    def job_count(self):
        """Returns the number of filtered jobs."""
        return self.get_queryset().count()

    def get_context_data(self, **kwargs):
        """Adds data to the template."""
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the saved for later jobs
        context["save_for_later"] = [
            i.job_id.job_id
            for i in Bookmark.objects.filter(user_id=self.request.user.id)
        ]
        context["jobs_applied"] = [
            i.job_id.job_id
            for i in Application.objects.filter(applicant_id=self.request.user.id)
        ]
        context["jobs_count"] = self.job_count()
        return context


def bookmark_call(request):
    """Create a new bookmark record in database."""
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

        # Check if there is a bookmark already
        bookmarks = Bookmark.objects.filter(user_id=user.id, job_id=job_id)
        bookmark_exists = len(bookmarks) == 0
        if not bookmark_exists:
            bookmarks.delete()

            return render(request, "htmx/bookmark.html", {"job": job})

        # Creates the bookmark
        new_bookmark = Bookmark(user_id=user, job_id=job)
        new_bookmark.save()

        return render(request, "htmx/bookmark-unmark.html", {"job": job})

    # If it is not POST
    raise Http404()


def apply_call(request):
    """Create a new application record in database."""
    if request.method == "POST":
        # Get the job ID or -1 if it is not found
        job_id = request.POST.get("job_id", -1)
        user = request.user

        # Check if the job ID is valid
        jobs = Job.objects.filter(pk=job_id)
        job_id_exists = len(jobs) == 1
        if not job_id_exists:
            raise Http404()

        # Check if there is an application already
        applications = Application.objects.filter(applicant_id=user.id, job_id=job_id)
        application_exists = len(applications) == 0
        if not application_exists:
            raise Http404()

        # Check if the job has been completed already
        if jobs[0].completed:
            raise Http404()

        # Check if the job has been cancelled already
        if jobs[0].hidden:
            raise Http404()

        # Create the application
        new_apply = Application(applicant_id=user, job_id=jobs[0])
        new_apply.save()

        # Send on site notification to the job poster
        # It lets them know that the job is ready to select an applicant
        # only sends once per job
        # Checks if the job poster allows on site notifications first
        if jobs[0].poster_id.opt_in_site_applicant:
            applications = Application.objects.filter(job_id=jobs[0], status="AP")
            if len(applications) < 2:
                Notification.objects.create(
                    user_id=jobs[0].poster_id,
                    title="Job is ready",
                    content="You can now choose an applicant for the job: "
                    + str(jobs[0].job_title),
                    link="/profile/me",
                )

        return render(request, "htmx/applied.html", {"job_id": job_id})

    # If it is not POST
    raise Http404()


def cancel_call(request):
    """Create a new application record in database."""
    if request.method == "POST":

        # Get the job ID or -1 if it is not found
        job_id = request.POST.get("job_id", -1)
        user = request.user

        # Check if the job ID is valid
        jobs = Job.objects.filter(pk=job_id, assigned=False, completed=False)
        job_id_exists = len(jobs) == 1
        if not job_id_exists:
            raise Http404()
        job = jobs[0]

        # Checks if the job has been cancelled already
        if job.hidden:
            raise Http404()

        # Hide the job
        job.hidden = True
        job.save()

        # Give the poster back the points
        user.frozen_balance -= job.points
        user.balance += job.points
        user.save()

        # Check if application exists
        applications = Application.objects.filter(
            Q(job_id=job_id) & ~Q(status="WD")
        )

        # Send on site notification to the applicants
        # It lets them know that the has been cancelled
        for application in applications:
            if application.applicant_id.opt_in_site_application:
                Notification.objects.create(
                    user_id=application.applicant_id,
                    title="Job Cancelled",
                    content="The job poster has cancelled the job: "
                    + str(job.job_title),
                    link="/profile/me",
                )

            application.status = "CA"
            application.time_of_final_status = timezone.now()
            application.save()

        # Redirect the user based on site they are on
        response = HttpResponse()

        if "profile/me" in request.META["HTTP_REFERER"]:
            response["HX-Redirect"] = request.META["HTTP_REFERER"]
        else:
            response["HX-Redirect"] = reverse("home")

        return response

    # If it is not POST
    raise Http404()
