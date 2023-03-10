# python inactivity.py - DO NOT RUN LOCALLY!!

import django

django.setup()

import os
import datetime
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db.models import Q
from chat.models import Message
from store.models import Moderation
from jobs.models import Job, Application


# Get actual user model.
User = get_user_model()


# The tokens for those users who signed up before this time and
#  they did not activate their account are expired.
old_time = datetime.datetime.now() - datetime.timedelta(seconds = settings.PASSWORD_RESET_TIMEOUT)

# Timezone aware time
tz = timezone.get_current_timezone()
time = timezone.make_aware(old_time, tz, True)

# Just delete those users
User.objects.filter(is_active=False, date_joined__lt=time).delete()


# Delete messages if it is enabled on Heroku
site = Site.objects.get_current().moderation
if site.chat_deletion:
    # Calculate time for messages to delete
    old_time = datetime.datetime.now() - datetime.timedelta(days = settings.CHAT_MESSAGE_TTL)

    # Timezone aware time
    time = timezone.make_aware(old_time, tz, True)

    # Just delete those messages
    Message.objects.filter(date_time__lt=time).delete()


# Hide jobs
jobs = Job.objects.filter(assigned=False, completed=False, hidden=False, deadline__lt=datetime.date.today())
for job in jobs:
    # Hide the job
    job.hidden = True
    job.save()

    # Give the poster back the points
    poster = job.poster_id
    poster.frozen_balance -= job.points
    poster.balance += job.points
    poster.save()

    # Check if application exists
    applications = Application.objects.filter(
        Q(job_id=job.job_id) &
        ~Q(status="WD")
    )

    # Send on site notification to the applicants
    # It lets them know that the has been cancelled

    for application in applications:

        if application.applicant_id.opt_in_site_application:
            Notification.objects.create(
                user_id=application.applicant_id,
                title="Job Cancelled",
                content="The job poster has cancelled the job: " + str(job.job_title),
                link="/profile/me"
            )

        application.status = "CA"
        application.time_of_final_status = timezone.now()
        application.save()
