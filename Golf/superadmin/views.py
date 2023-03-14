import random
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

from django.db import models
from django.db.models import Q
from .models import ReportTicket,Report

from django.views import View
from django.views.generic import ListView
from store.models import Moderation
from userprofile.models import User, Notification

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
             # directly dealt with by admins?
            if len(eligible) >= 3:
                reviewers = random.sample(list(eligible), k=3)

                for reviewer in reviewers:
                    ticket = ReportTicket.objects.create(
                        report_id = report,
                        user_id = reviewer,
                    )
                    ticket.save()

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


def conflict_call(request):
    """ Called when a superuser submits a verdict on a ticket """
    if request.method == "POST":
        # Get the ticket ID or -1 if it is not found
        ticket_id = request.POST.get("ticket_id", -1)
        user = request.user

        # Check if the ticket ID is valid
        ticket = ReportTicket.objects.filter(pk=ticket_id)
        ticket_id_exists = len(ticket) == 1
        if not ticket_id_exists:
            raise Http404()

        # Obtains the superusers verdict from the button submit hx vals
        answer = request.POST.get('answer')

        # Assigns and saves the verdict to the ticket on the DB
        if answer == 'Guilty':
            ticket[0].answer = "BA"
        elif answer == 'Not Guilty':
            ticket[0].answer = "NB"
        ticket[0].save()

        # Queries the reported job for a list of all answers
        verdict = ReportTicket.objects.filter(
                Q(report_id=ticket[0].report_id) &
                ~Q(answer=None)
        )

        # if length of verdict is 3, we have all responses back from superusers
        if len(verdict) == 3:
            ban = 0
            for x in range(0, len(verdict)):
                # Counts the number of answers for banning the user
                if verdict[x].answer == 'BA':
                    ban += 1

                # Update the ticket status to resolved
                verdict[x].status = 'RE'
                verdict[x].save()

            # If two or more superusers voted for ban
            if ban >= 2:

                # NEEDS TO HIDE OR REMOVE THE OFFENDING JOB 
                # BUT THERE ARE MANY IMPLICATIONS TO DOING THAT

                # Bans the offending user by removing site privileges
                # There are once again many implications to doing this
                ticket[0].report_id.reported_user.is_active = 0

                # Saves the User model
                ticket[0].report_id.reported_user.save()

                # Used to store the decision state for the notification
                verdictmessage = "guilty"
            else:
                verdictmessage = "not guilty"

            # Sets the status of the report to resolved
            ticket[0].report_id.status = 'Resolved'

            # Saves the Report model
            ticket[0].report_id.save()

            # Obtains the model for the entire website
            sitemodel = Moderation.objects.get(site=get_current_site(request).id)

            # Distributes scrip to the superusers, from the bank
            for x in range(0, len(verdict)):
                # Takes the scrip from the bank
                sitemodel.bank -= 2
                
                # Gives the scrip to the superuser
                verdict[x].user_id.balance += 2
                verdict[x].user_id.save()

            # Prints scrip if bank runs out
            if sitemodel.bank < 0:
                sitemodel.bank = 0
            
            # Saves the new bank state
            sitemodel.save()

            # Sends out a notification to all superusers to let them know the status of the conflict
            for x in range(0, len(verdict)):
                Notification.objects.create(
                    user_id=verdict[x].user_id,
                    title="Report resolved",
                    content="Thank you for responding to ticket: "
                    + str(ticket[0].ticket_id) + ". The results are back and the"
                    + " system has found the offending user " + verdictmessage +
                    ". You have been awarded two doos for your service.",
                    link="/superadmin/",
                )
            
        return render(request, "htmx/verdictclosed.html", {"ticket":ticket_id, "answer":answer})

    # In the case that request method is not POST
    raise Http404()
