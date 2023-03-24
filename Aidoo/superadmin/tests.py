from faker import Faker
import datetime
import random
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from Aidoo.utils import LoginRequiredTestCase, fake_time
from jobs.models import Job
from superadmin.models import Report, ReportTicket, ConflictResolution
from superadmin.forms import ReportForm


# Get actual user model.
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
            credentials["profile_id"] = "media/profilepics/default"
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
        """Create user and a job before every test."""

        #user
        credentials = {
            "username": "asd",
            "password": "asd123",
            "date_of_birth": datetime.datetime.now(),
            "profile_id": "media/profilepics/default",
        }
        User.objects.create_user(**credentials)

        #job
        job = dict()
        job["posting_time"] = fake_time()
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


class ReportTicketTestCase(TestCase):
    """Ticket model test"""

    def setUp(self):
        fake = Faker()

        # create 1 user in the database
        credentials = dict()
        credentials["username"] = fake.unique.name()
        credentials["password"] = "a"
        credentials["last_name"] = lambda: fake.last_name()
        credentials["first_name"] = lambda: fake.first_name()
        credentials["date_of_birth"] = fake_time()
        credentials["profile_id"] = "media/profilepics/default"
        self.user = User.objects.create_user(**credentials)

        #create job
        job = {
            "poster_id": self.user,
            "location": "AB21 3EW",
            "job_title": "Walking a dog",
            "job_description": "Nothing",
            "points": 10,
        }
        Job.objects.create(**job)
        j = Job.objects.get(pk=1)

        #create report
        report = {
            "reported_job": j,
            "reported_user": self.user,
            "reporting_user": self.user,
            "complaint": "a"*500,
            "status": 'OPEN',
            "type": 'JOB'
        }
        Report.objects.create(**report)
        r = Report.objects.get(pk=1)

        #create ticket
        ticket = {
            "report_id": r,
            "user_id": self.user,
        }
        ReportTicket.objects.create(**ticket)

    def test_insertion(self):
        #insert ticket
        j = Job.objects.get(pk=1)
        r = Report.objects.get(pk=1)
        t = ReportTicket.objects.get(pk=1)

        len1 = len(ReportTicket.objects.all())
        ticket = {
            "report_id": r,
            "user_id": self.user,
        }

        ReportTicket.objects.create(**ticket)

        len2 = len(ReportTicket.objects.all())

        self.assertEqual(len1+1, len2)

    def test_deletion(self):
        #delete ticket
        len1 = len(ReportTicket.objects.all())

        t = ReportTicket.objects.get(pk=1)
        t.delete()

        len2 = len(ReportTicket.objects.all())

        self.assertEqual(len1-1, len2)

    def test_resolution(self):
        #change status of the ticket
        pass


class ConflictRersolutionTestCase(TestCase):

    def setUp(self):
        fake = Faker()

        # create 1 user in the database
        credentials = dict()
        credentials["username"] = fake.unique.name()
        credentials["password"] = "a"
        credentials["last_name"] = lambda: fake.last_name()
        credentials["first_name"] = lambda: fake.first_name()
        credentials["date_of_birth"] = fake_time()
        credentials["profile_id"] = "media/profilepics/default"
        self.user = User.objects.create_user(**credentials)

        #create job
        job = {
            "poster_id": self.user,
            "location": "AB21 3EW",
            "job_title": "Walking a dog",
            "job_description": "Nothing",
            "points": 10,
        }
        Job.objects.create(**job)
        j = Job.objects.get(pk=1)

        conflict = {
            "job_id": j,
            "user1_id": self.user,
            #"user2_id":self.user,
            "content": "a"*50,
            "status": 'OPEN',
            "type": 'CONFLICT1'
        }
        ConflictResolution.objects.create(**conflict)

    def test_insertion(self):
        #insert conflict
        j = Job.objects.get(pk=1)

        len1 = len(ConflictResolution.objects.all())

        conflict = {
            "job_id": j,
            "user1_id": self.user,
            #"user2_id":self.user,
            "content": "a"*50,
            "status": 'OPEN',
            "type": 'CONFLICT1'
        }
        ConflictResolution.objects.create(**conflict)

        len2 = len(ConflictResolution.objects.all())
        self.assertEqual(len1+1, len2)

    def test_deletion(self):
        #delete a conflict
        len1 = len(ConflictResolution.objects.all())

        conflict = ConflictResolution.objects.get(pk=1)
        conflict.delete()

        len2 = len(ConflictResolution.objects.all())

        self.assertEqual(len1-1, len2)

    def test_resolution(self):
        #change status of the conflict
        pass

    def test_content_max_length(self):
        j = Job.objects.get(pk=1)

        conflict = {
            "job_id": j,
            "user1_id": self.user,
            #"user2_id":self.user,
            "content": "a"*500,
            "status": 'OPEN',
            "type": 'CONFLICT1'
        }

        created_conflict = ConflictResolution.objects.create(**conflict)

        with self.assertRaises(ValidationError):
            created_conflict.full_clean()


class ReportsViewTestCase(LoginRequiredTestCase):
    """Tests for the reporting page"""   

    def test_report_view(self):
        response = self.client.get("/superadmin/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="superadmin/index.html")

    def test_report_view_available_by_name(self):
        response = self.client.get(reverse("superadmin"))
        self.assertEqual(response.status_code, 200)

class ConflictCallTestCase(LoginRequiredTestCase):
    """Tests for when a user submits a verdict on a report"""

    def setUp(self):
        fake = Faker()

        # login from super...
        super().setUp()

        # create 1 user in the database
        credentials = dict()
        credentials["username"] = fake.unique.name()
        credentials["password"] = "a"
        credentials["last_name"] = lambda: fake.last_name()
        credentials["first_name"] = lambda: fake.first_name()
        credentials["date_of_birth"] = fake_time()
        credentials["profile_id"] = "media/profilepics/default"
        self.user = User.objects.create_user(**credentials)

        #create job
        job = {
            "poster_id": self.user,
            "location": "AB21 3EW",
            "job_title": "Walking a dog",
            "job_description": "Nothing",
            "points": 10,
        }
        Job.objects.create(**job)
        j = Job.objects.get(pk=1)

        #create report
        report = {
            "reported_job": j,
            "reported_user": self.user,
            "reporting_user": self.user,
            "complaint": "a"*500,
            "status": 'OPEN',
            "type": 'JOB'
        }
        Report.objects.create(**report)
        r = Report.objects.get(pk=1)

        #create ticket
        ticket = {
            "report_id": r,
            "user_id": self.user,
        }
        ReportTicket.objects.create(**ticket)
    
    def test_page(self):
        # test availability via URL
        response = self.client.get("/superadmin/conflict")
        self.assertEqual(response.status_code, 404)

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("conflict"))
        self.assertEqual(response.status_code, 404)

    def test_no_ticket_id(self):
        # test without sending a ticket id
        response = self.client.post("/superadmin/conflict")
        self.assertEqual(response.status_code, 404)
    
    def test_wrong_ticket_id(self):
        # test with wrong ticket id
        response = self.client.post("/superadmin/conflict", {"ticket_id": 2})
        self.assertEqual(response.status_code, 404)

    def test_ticket_resolved_already(self):
        # test with a ticket that is already resolved
        ticket = ReportTicket.objects.get(ticket_id='1')
        ticket.status = 'RE'
        ticket.save()

        response = self.client.post("/superadmin/conflict", {"ticket_id": 1})
        self.assertEqual(response.status_code, 404)
    
    def test_report_resolved(self):
        # test works
        response = self.client.post("/superadmin/conflict", {"ticket_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="htmx/verdictclosed.html")
