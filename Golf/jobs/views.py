from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Job, Bookmark, Application
from .forms import JobForm
from userprofile.models import Notification


# Get actual user model.
User = get_user_model()


def details(request, job_id):
    """Shows the details of a job. It is a static page."""

    # Read the job from the database
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        raise Http404("This job does not exist.")

    # Temporary measure until I figure out how to connect the jobs view to the jobsdetail
    jobs_applied = [
        i.job_id.job_id
        for i in Application.objects.filter(applicant_id=request.user.id)
    ]

    # Give the found job to the template
    context = {
        "job": job,
        "jobs_applied": jobs_applied
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
            request, self.template_name, {"form": form, "poster_id": request.user.id}
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # Recalculate points (because of security - the user could change the calculated value)
            duration_days = form.cleaned_data["duration_days"]
            duration_hours = form.cleaned_data["duration_hours"]
            post = form.save(commit=False)
            post.points = (duration_days * 24 + duration_hours) * 5
            post.save()

            # Freeze points
            me = request.user
            me.frozen_balance = me.frozen_balance + post.points
            me.balance = me.balance - post.points
            me.save()

            return HttpResponse(status=204) # No content

        return render(
            request, self.template_name, {"form": form, "poster_id": request.user.id}
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
            Q(job_title__icontains=filter_val) |
            Q(job_description__icontains=filter_val) |
            Q(location__icontains=filter_val),
            hidden=False,
            assigned=False
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

        # Check if there is a bookmark already
        bookmarks = Bookmark.objects.filter(user_id=user.id,job_id=job_id)
        bookmark_exists = len(bookmarks) == 0

        if not bookmark_exists:
            bookmarks.delete()

            return render(
                request, "htmx/bookmark.html", {"job": jobs[0]}
            )

        # Creates the bookmark
        new_bookmark = Bookmark(user_id=user, job_id=jobs[0])
        new_bookmark.save()

        return render(
            request, "htmx/bookmark-unmark.html", {"job": jobs[0]}
        )

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

        # Create the application
        new_apply = Application(applicant_id=user, job_id=jobs[0])
        new_apply.save()

        # Send on site notification to the job poster when a user applies
        # Checks if the job poster allows on site notifications first

        if jobs[0].poster_id.opt_in_site_applicant == True:
            Notification.objects.create(
                user_id=jobs[0].poster_id,
                content=str(user.username) + " applied to your job: " + str(jobs[0].job_title),
                link="/profile/me"
                )
        
        return render(
            request, "htmx/applied.html", {"job_id": job_id}
        )

    # If it is not POST
    raise Http404()


def report_call(request):
    """Do something related to reporting a job post TBD."""
    if request.method == "POST":
        # Get the job ID or -1 if it is not found
        job_id = request.POST.get("job_id", -1)

        # Check if the job ID is valid
        jobs = Job.objects.filter(pk=job_id)
        job_id_exists = len(jobs) == 1
        if not job_id_exists:
            raise Http404()

        # Since this functionality is not yet implemented, we have to send back
        # the job to be able to click again, as it was possible with JS.
        return render(
            request, "htmx/report-alert.html", {"job": jobs[0]}
        )

    # If it is not POST
    raise Http404()
