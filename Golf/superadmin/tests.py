from faker import Faker
import datetime
import random
from django.utils.html import strip_tags
from django.test import TestCase
from django.utils import timezone
from Golf.utils import LoginRequiredTestCase
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job
from superadmin.models import Report
from superadmin.forms import ReportForm

User = get_user_model()

class ReportingTestCase(LoginRequiredTestCase):
    """ tests for the reports model """

    def setUp(self):
        # Login from super
        # require being logged in
        super().setUp()

        # prepare for adding reports
        # users
        fake = Faker()
        # write 10 users into the table
        for i in range(10):
            credentials = dict()
            credentials["username"] = fake.unique.name()
            credentials["password"] = "a"
            credentials["last_name"] = lambda: fake.last_name()
            credentials["first_name"] = lambda: fake.first_name()
            credentials["date_of_birth"] = datetime.datetime.now()
            User.objects.create_user(**credentials)
            credentials.clear()

        # jobs
        job = {
            "poster_id": self.user,
            "location": "AB21 3EW",
            "job_title": "Walking a dog",
            "job_description": "Nothing",
            "points": 10,
        }
        Job.objects.create(**job)

        j = Job.objects.get(pk=1)

        r = {
            "reported_job": j,
            "reported_user": self.user,
            "reporting_user": self.user,
            "complaint": "a"*500,
            "status": 'OPEN',
            "type": 'JOB'
        }
        Report.objects.create(**r)




    def test_insertion(self):
        # insert a report
        j = Job.objects.get(pk=1)
        len1 = len(Report.objects.all())

        r = {
            "reported_job": j,
            "reporting_user": self.user,
            "reported_user": self.user,
            "complaint": "a"*500,
            "status": 'OPEN',
            "type": 'JOB'
        }
        Report.objects.create(**r)

        len2 = len(Report.objects.all())

        self.assertEqual(len1 + 1, len2)

    def test_deletion(self):
        # delete a report
        len1 = len(Report.objects.all())

        r = Report.objects.get(pk=1)
        r.delete()

        len2 = len(Report.objects.all())

        self.assertEqual(len1 - 1, len2)
        pass

    def test_resolution(self):
        # change the status of the report
        pass


    def test_complaint_max_length(self):
        j = Job.objects.get(pk=1)
        len1 = len(Report.objects.all())

        r = {
            "reported_job": j,
            "reporting_user": self.user,
            "reported_user": self.user,
            "complaint": "a"*5000,
            "status": 'OPEN',
            "type": 'JOB'
        }
        created_report = Report.objects.create(**r)

        with self.assertRaises(ValidationError):
            created_report.full_clean()

class PostReportCase(TestCase):
    """Tests for reporting a job."""

    def fake_time(self):
        """Returns a timezone aware time to prevent warnings."""
        fake = Faker()
        tz = timezone.get_current_timezone()
        return timezone.make_aware(fake.date_time(), tz, True)

    def setUp(self):
        """Create user and a job before every test."""

        #user
        credentials = {
            "username": "asd",
            "password": "asd123",
            "date_of_birth": datetime.datetime.now(),

        }
        User.objects.create_user(**credentials)

        #job
        job = dict()
        job["posting_time"] = self.fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = 1
        Job.objects.create(**job)
    
    def test_empty_form(self):

        job = Job.objects.get(pk=1)
        #behaviour if empty form is submitted
        form = ReportForm(data={})
        self.assertEqual(5, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required", form.errors[key][0])


    def test_added_complaint(self):
        new_report = {
            "reporting_user": "1",
            "reported_user": "1",
            "reported_job": Job.objects.get(pk=1),
            "complaint": "!"*11, 
            "type":"Job"
        }
        form = ReportForm(data=new_report)

        #No errors.
        self.assertEqual(0, len(form.errors))

    def test_complaint_too_short(self):
        #complaint has not enough characters
        new_report = {
            "reporting_user": "1",
            "reported_user": "1",
            "reported_job": Job.objects.get(pk=1),
            "complaint": "!",
            "type":"Job"
        }
        form = ReportForm(data=new_report)
        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("Ensure this value has at least 10 characters (it has 1).", form.errors[key][0])

    def test_complaint_too_long(self):
        #complaint is exceeding character limit
        new_report = {
            "reporting_user": "1",
            "reported_user": "1",
            "reported_job": Job.objects.get(pk=1),
            "complaint": "!"*1001,
            "type":"Job"
        }
        form = ReportForm(data=new_report)
        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("Ensure this value has at most 1000 characters", form.errors[key][0])

