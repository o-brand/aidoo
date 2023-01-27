from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Job, Bookmark, Application
from .forms import JobForm


# Get actual user model.
User = get_user_model()


def details(request, job_id):
    """Shows the details of a job. It is a static page."""

    # Read the job from the database
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        raise Http404("This job does not exist.")

    # Give the found job to the template
    context = {
        "job": job,
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

            return redirect("/jobs/")

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
        filter_val = self.request.GET.get("search_title", "")
        return Job.objects.filter(
            Q(job_title__icontains=filter_val) |
            Q(job_description__icontains=filter_val) |
            Q(job_short_description__icontains=filter_val) |
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
    user_id = int(request.POST["uid"])
    job_id = int(request.POST["jid"])

    try:
        u = Bookmark.objects.get(user_id=user_id, job_id=job_id)
    except Bookmark.DoesNotExist:
        new_bookmark = Bookmark(  # Make new Bookmark record
            user_id=User.objects.get(pk=user_id), job_id=Job.objects.get(pk=job_id)
        )
        new_bookmark.save()  # Save new Bookmark record in database table
    else:
        u.delete()
    finally:
        return HttpResponse("ok")


def apply_call(request):
    """Create a new application record in database."""
    uid = int(request.POST["uid"])
    jid = int(request.POST["jid"])

    try:
        u = Application.objects.get(applicant_id=uid, job_id=jid)
    except Application.DoesNotExist:
        new_apply = Application(
            applicant_id=User.objects.get(pk=uid),
            job_id=Job.objects.get(pk=jid),
        )
        new_apply.save()
    finally:
        return HttpResponse("ok")


def report_call(request):
    """Do something related to reporting a job post TBD."""
    return HttpResponse("ok")


# This is used in generic_call to map a string to a function.
function_dict = {"bookmark": bookmark_call, "app": apply_call, "report": report_call}


def generic_call(request):
    """Run a function from dict as specified by the request on the front end."""
    return function_dict[request.POST["func"]](request)
    # Make sure that your functions return HttpResponse object or similar
