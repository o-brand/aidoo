from faker import Faker
import datetime
from django.test import TestCase
from Golf.utils import LoginRequiredTestCase
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job
from superadmin.models import Report

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

        


