import random
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views import View
from .forms import ReportForm
from .models import Report #, ReportTicket


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
            me = request.user
            actual_user_id = me.id

            report = form.save(commit=False)
            report.save()

            eligible = User.objects.filter(
                 Q(charity=False) &
                 Q(super_user=True) &
                 ~Q(id=actual_user_id) &
                 ~Q(id=report.reported_user.id)
            )
            
             # TODO not sure what to do when there aren't enough eligible reviewers
             # Should we have a script to ticket it when there are? Or should it be
             # direcrly dealt with by admins?
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
