import random
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.db import models
from django.db.models import Q
from .models import ReportTicket,Report

from django.views import View
from django.views.generic import ListView
from userprofile.models import User

from .forms import ReportForm

# Get actual user model.
User = get_user_model()

def home(request):
    # Render the page
    return render(request, "superadmin/index.html")


class ReportFormView(View):
    """Displays form to report a job post"""

    form_class = ReportForm
    template_name = "postreport.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request, self.template_name, {
                "form": form,
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            post = form.save(commit=False)
            post.save()
            superadmin_user = User.objects.filter(super_user=True)
            Random = random.randint(0,superadmin_user.count())
            random_superadmin_user = superadmin_user[Random]
            ReportTicket.objects.create(
                user_id = random_superadmin_user,
                report_id = post,
            )
            
            me = request.user
            actual_user_id = me.id

            report = form.save(commit=False)
            report.save()

            # please explain the logic of this in a comment
            # why bitwise not?
            # what is Q?
            # why does this result in eligable users
            eligible = User.objects.filter(
                 Q(charity=False) &
                 Q(super_user=True) &
                 ~Q(id=actual_user_id) &
                 ~Q(id=report.reported_user.id)
            )
            
             # TODO not sure what to do when there aren't enough eligible reviewers
             # Should we have a script to ticket it when there are? Or should it be
             # directly dealt with by admins?
            if len(eligible) >= 3:
                reviewers = random.sample(list(eligible), k=3)

                # TODO Uncomment when ticket model is added to main branch

                # for reviewer in reviewers:
                #     ticket = ReportTicket.objects.create(
                #         report_id = report,
                #         user_id = reviewer,
                #     )
                #     ticket.save()

                report.status = Report.ReportStatus.TICKETED
                report.save()

            return HttpResponse(status=204)

        return render(
            request, self.template_name, {"form": form,
                "reporting_user": request.user.id,
                "reported_job": request.POST.get("job_id"),
                "reported_user":request.POST.get("user_id")},
        )

class ReportsView(ListView):
    """Displays a list to show the reports."""

    model = ReportTicket
    template_name = "superadmin/index.html"
    context_object_name = "tickets"

    def get_queryset(self):
        """Reads reports from the database."""
        me = self.request.user
        tickets = ReportTicket.objects.filter(user_id=me)

        return tickets
