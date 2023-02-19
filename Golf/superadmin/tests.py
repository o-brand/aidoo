from faker import Faker
import datetime
from django.test import TestCase
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

    def setUp(self):
        """Create user before every test."""
        credentials = {
            "username": "asd",
            "password": "asd123",
            "date_of_birth": datetime.datetime.now(),

        }
        User.objects.create_user(**credentials)
    
    def test_empty_form(self):
        #behaviour if empty form is submitted
        form = ReportForm(data={"reporting_user": "1",
            "reported_user": "1",
            "reported_job": "1", })

        self.assertEqual(1, len(form.errors))
        self.assertIn("This field is required", form.errors[0])
        print("empty")

    def test_added_complaint(self):
        new_report = {
            "reporting_user": "1",
            "reported_user": "1",
            "reported_job": "1",
            "complaint": "!"*11, 
        }
        form = ReportForm(data=new_report)

        #No errors.
        self.assertEqual(0, len(form.errors))
        print("ok")

    def test_complaint_too_short(self):
        #complaint has not enough characters
        new_report = {
            "reporting_user": "1",
            "reported_user": "1",
            "reported_job": "1",
            "complaint": "!",
        }
        form = ReportForm(data=new_application)
        self.assertEqual(1, len(form.errors))
        self.assertIn("Ensure this field has at least 10 characters", form.errors[0])
        print("short")


    def test_complaint_too_long(self):
        #complaint is exceeding character limit
        new_report = {
            "reporting_user": "1",
            "reported_user": "1",
            "reported_job": "1",
            "complaint": "!"*1001,
        }
        form = ReportForm(data=new_report)

        self.assertEqual(1, len(form.errors))
        self.assertIn("Ensure this value has at most 1000 characters", form.errors[0])
        print("long")


        


