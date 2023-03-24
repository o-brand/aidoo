import random
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone

from django.db import models
from django.db.models import Q
from .models import ReportTicket,Report

from django.views import View
from django.views.generic import ListView
from store.models import Moderation
from userprofile.models import User, Notification
from jobs.models import Application

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

            moderation = get_current_site(request).moderation

            eligible = User.objects.filter(
                Q(charity=False) &
                Q(guardian=True) &
                ~Q(id=actual_user_id) &
                ~Q(id=report.reported_user.id) &
                ~Q(id=report.reporting_user.id)
            )

             # TODO not sure what to do when there aren't enough eligible reviewers
             # Should we have a script to ticket it when there are? Or should it be
             # directly dealt with by admins?
            if len(eligible) >= 3:
                outsourceable = min(
                    moderation.bank // moderation.ticket_payout, 3)
                out_reviewers = random.sample(
                    list(eligible.filter(is_staff=False)), k=outsourceable)
                in_reviewers = random.sample(
                    list(eligible.filter(is_staff=True)), k=3-outsourceable)
                reviewers = out_reviewers + in_reviewers

                for reviewer in reviewers:
                    ticket = ReportTicket.objects.create(
                        report_id = report,
                        user_id = reviewer,
                    )
                    ticket.save()

                    notification = Notification.objects.create(
                        user_id = reviewer,
                        title = "New Guardian assignment",
                        content = ("You have been assigned to a new Guardian "
                        "task. Please review the evidence and provide your "
                        "response promptly."),
                        link = "/superadmin/",
                    )
                    notification.save()

                    if not reviewer.is_staff:
                        moderation.bank -= moderation.ticket_payout
                        moderation.bank.save()
                        moderation.frozen_bank += moderation.ticket_payout
                        moderation.frozen_bank.save()
                        
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
        
        # Check if the ticket ID is valid
        ticket = ReportTicket.objects.filter(pk=ticket_id)
        ticket_id_exists = len(ticket) == 1
        if not ticket_id_exists:
            raise Http404()

        ticket[0].report_id
        # Checks if the ticket has already been resolved
        if ticket[0].status == 'RE':
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

        # Context for template, used by htmx
        verd = "• Verdict: Awaiting decision from other users..."

        # if length of verdict is 3, we have all responses back from superusers
        if len(verdict) == 3:
            ban = 0
            for x in range(0, len(verdict)):
                # Counts the number of answers for banning the user
                if verdict[x].answer == 'BA':
                    ban += 1

            # If two or more superusers voted for ban
            if ban >= 2:

                # BAN CASE: Remove the job from the site, by running the cancel 
                # call
                # In the case that the job has accepted an applicant already
                # we hide the job and give the scrip to the applicant
                
                # Checks if the job has been cancelled already
                if ticket[0].report_id.reported_job.hidden == False:
    
                    # Hide the job
                    ticket[0].report_id.reported_job.hidden = True
                    ticket[0].report_id.reported_job.save()
                    
                    # Check if job has been completed already
                    if ticket[0].report_id.reported_job.completed == False:
                        # Check if an applicant was accepted
                        applications = Application.objects.filter(
                            job_id=ticket[0].report_id.reported_job.job_id,
                            status='AC'
                            )

                        # Variables for job poster object
                        # and the reported job object
                        poster = ticket[0].report_id.reported_job.poster_id
                        reportedjob = ticket[0].report_id.reported_job

                        # points distribution
                        if len(applications) > 0:
                            # Give the applicant the points
                            poster.frozen_balance -= reportedjob.points
                            applications[0].applicant_id.balance += reportedjob.points
                            applications[0].applicant_id.save()
                        else:  
                            # Give the poster back the points
                            poster.frozen_balance -= reportedjob.points
                            poster.balance += reportedjob.points

                        # Saves the balance of the poster
                        poster.save()

                        # Check if application exists
                        applications = Application.objects.filter(
                            Q(job_id=ticket[0].report_id.reported_job.job_id) & 
                            ~Q(status="WD")
                        )

                        # Send on site notification to the applicants
                        # It lets them know that the has been cancelled

                        for application in applications:
                            if application.applicant_id.opt_in_site_application:
                                Notification.objects.create(
                                    user_id=application.applicant_id,
                                    title="Job Cancelled",
                                    content=("The following job has been cancelled: "
                                    f"{ticket[0].report_id.reported_job.job_title}"),
                                    link="/profile/me",
                                )

                            application.status = "CA"
                            application.time_of_final_status = timezone.now()
                            application.save()

                # Saves the status of the report
                ticket[0].report_id.answer = 'BA'

                # Used to store the decision state for the notification
                verdictmessage = "guilty"

                # Context for template, used by htmx
                verd = "• Verdict: Banned"
            else:
                # Saves the status of the report
                ticket[0].report_id.answer = 'NB'

                # Context for template, used by htmx
                verd = "• Verdict: Not Banned"

                verdictmessage = "not guilty"

            # Sets the status of the report to resolved
            ticket[0].report_id.status = 'Resolved'

            # Saves the Report model
            ticket[0].report_id.save()

            # Obtains the model for the entire website
            sitemodel = Moderation.objects.get(site=get_current_site(request).id)

            # Distributes scrip to the superusers, from the bank
            for x in range(0, len(verdict)):
                # Takes the scrip from the bank and gives it to the guardian
                if not verdict[x].user_id.is_staff:
                    sitemodel.frozen_bank -= sitemodel.ticket_payout
                    verdict[x].user_id.balance += sitemodel.ticket_payout
                    verdict[x].user_id.save()

            # Saves the new bank state
            sitemodel.save()

            # Sends out a notification to all superusers to let them 
            # know the status of the conflict
            for x in range(0, len(verdict)):
                notification = Notification.objects.create(
                    user_id = verdict[x].user_id,
                    title = "Report resolved",
                    content = ("Thank you for responding to ticket: "
                    f"{verdict[x].ticket_id}. The results are back and the"
                    f" system has found the offending user {verdictmessage}"
                    ". You have been awarded 2 doos for your service."),
                    link="/superadmin/",
                )
                notification.save()
            
            # Sends out a notification to the user who filed the complaint
            notification = Notification.objects.create(
                user_id = ticket[0].report_id.reporting_user,
                title = "Report resolved",
                content = ("Thank you for helping keep Aidoo safe."
                " The verdict is back and the"
                f" system has found the offending user {verdictmessage}"),
                link="/jobs/",
            )
            notification.save()

        # Mark the ticket as closed
        ticket[0].status = 'RE'
        ticket[0].save()
            
        return render(request, "htmx/verdictclosed.html", 
                      {"ticket":ticket_id, "answer":answer, "verd":verd})

    # In the case that request method is not POST
    raise Http404()
