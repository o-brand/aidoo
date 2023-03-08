from faker import Faker
import datetime
import random
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.test import TestCase
from Golf.utils import LoginRequiredTestCase, fake_time
from jobs.models import Job, Application
from userprofile.models import Notification
from .forms import ProfileEditForm


# Get actual user model.
User = get_user_model()


class UserTableTestCase(TestCase):
    """ Testing the User Model"""

    def setUp(self):
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

    def test_retrieve_user(self):

        u = User.objects.get(pk=1)

        self.assertEqual(u.id, 1)

    def test_create_user(self):
        fake = Faker()
        len1 = len(User.objects.all())

        credentials = dict()
        credentials["username"] = "123"
        credentials["password"] = "a"
        credentials["last_name"] = lambda: fake.last_name()
        credentials["first_name"] = lambda: fake.first_name()
        credentials["date_of_birth"] = datetime.datetime.now()
        User.objects.create_user(**credentials)

        len2 = len(User.objects.all())

        self.assertEqual(len1+1, len2)

    def test_delete_user(self):
        u = User.objects.get(pk=1)
        len1 = len(User.objects.all())

        u.delete()

        len2 = len(User.objects.all())

        self.assertEqual(len1-1, len2)

    def test_balance(self):
        # checks if the balance is greater or equal to 0
        # assumes that there are no negative values allowed
        u = User.objects.get(pk=1)
        self.assertGreaterEqual(u.balance, 0)

    def test_DoB(self):
        # tests if there are 3 items separated by "-"
        u = User.objects.get(pk=1)
        l = str(u.date_of_birth).split("-")
        Y = int(l[0])
        M = int(l[1])
        D = int(l[2])
        self.assertEqual(type(datetime.date(Y,M,D)), datetime.date)

    def test_rating(self):
        # checks if the rating is greater or equal than 0
        u = User.objects.get(pk=1)
        self.assertGreaterEqual(u.rating, 0)

    def test_email_preferences_application(self):
        # checks if the email preference exists and is either True or False
        # for notification to user when accepted or rejected from a job
        u = User.objects.get(pk=1)
        self.assertIn(u.opt_in_emails_application, {True:False})

    def test_site_preferences_application(self):
        # checks if the site preference exists and is either True or False
        # for notification to user when accepted or rejected from a job
        u = User.objects.get(pk=1)
        self.assertIn(u.opt_in_site_application, {True:False})

    def test_site_preferences_applicant(self):
        # checks if the site preference exists and is either True or False
        # for notification to job poster when user applies for their job
        u = User.objects.get(pk=1)
        self.assertIn(u.opt_in_site_applicant, {True:False})


class PublicProfileTestCase(LoginRequiredTestCase):
    """Tests for the PUBLIC profile page."""

    def test_profile(self):
        response = self.client.get("/profile/" + str(self.user.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="userprofile/public.html")

    def test_profile_available_by_name(self):
        response = self.client.get(reverse("userdetails", kwargs={"user_id":self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_profile_404(self):
        response = self.client.get("/profile/0")
        self.assertEqual(response.status_code, 404)


class PrivateProfileTestCase(LoginRequiredTestCase):
    """Tests for the PRIVATE profile page."""

    def test_profile(self):
        response = self.client.get("/profile/me")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="userprofile/private.html")

    def test_profile_available_by_name(self):
        response = self.client.get(reverse("me"))
        self.assertEqual(response.status_code, 200)


class WithdrawButtonCase(LoginRequiredTestCase):
    """Tests for withdraw button."""

    def setUp(self):
        # Login from super...
        super().setUp()

        # Write 1 job into the job model
        for i in range(2):
            job = dict()
            job["posting_time"] = fake_time()
            job["points"] = random.randint(0, 100)
            job["assigned"] = False
            job["completed"] = False
            job["poster_id_id"] = 1
            Job.objects.create(**job)

        # Write 1 application into the application model
        application = dict()
        application["applicant_id"] = User(pk=1)
        application["job_id"] = Job(pk=1)
        application["status"] = "AP"
        Application.objects.create(**application)

    def test_page(self):
        # test availability via URL
        response = self.client.get("/profile/withdraw")
        self.assertEqual(response.status_code, 404)

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("withdraw"))
        self.assertEqual(response.status_code, 404)

    def test_page_post_no_job(self):
        # test without sending a job id
        response = self.client.post("/profile/withdraw")
        self.assertEqual(response.status_code, 404)

    def test_page_post_job_not_valid(self):
        # test with a wrong job id
        response = self.client.post("/profile/withdraw", {"job_id": 5})
        self.assertEqual(response.status_code, 404)

    def test_page_post_job_no_application_exists(self):
        # test with an application which does not exist
        response = self.client.post("/profile/withdraw", {"job_id": 2})
        self.assertEqual(response.status_code, 404)

    def test_page_post_job(self):
        # test works
        response = self.client.post("/profile/withdraw", {"job_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="htmx/job-applied.html")
        self.assertEqual(Application.objects.get(applicant_id=self.user.id,job_id=1).status, "WD")


class SelectApplicantButtonCase(LoginRequiredTestCase):
    """Tests for selecting an applicant button."""

    def setUp(self):
        # Login from super...
        super().setUp()

        # Write 2 job into the job model
        job = dict()
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = 1
        Job.objects.create(**job)

    def test_page(self):
        # test availability via URL
        response = self.client.get("/profile/selectapplicant")
        self.assertEqual(response.status_code, 404)

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("selectapplicant"))
        self.assertEqual(response.status_code, 404)

    def test_page_post_no_job(self):
        # test without sending a job id
        response = self.client.post("/profile/selectapplicant")
        self.assertEqual(response.status_code, 404)

    def test_page_post_job_not_valid(self):
        # test with a wrong job id
        response = self.client.post("/profile/selectapplicant", {"job_id": 5})
        self.assertEqual(response.status_code, 404)

    def test_page_post_user_not_valid(self):
        # test with a wrong user id
        response = self.client.post("/profile/selectapplicant", {"accept": 5})
        self.assertEqual(response.status_code, 404)

    def test_page_post_job_no_application_exists(self):
        # test with an application which does not exist
        response = self.client.post("/profile/selectapplicant", {"job_id": 2, "accept": 2})
        self.assertEqual(response.status_code, 404)

    def test_page_post_job(self):
        # test works
        fake = Faker()

        # Create a new job
        job = dict()
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = 1
        job_object = Job.objects.create(**job)

        # Create a user
        credentials = dict()
        credentials["username"] = fake.unique.name()
        credentials["password"] = "a"
        credentials["last_name"] = lambda: fake.last_name()
        credentials["first_name"] = lambda: fake.first_name()
        credentials["date_of_birth"] = datetime.datetime.now()
        user2 = User.objects.create_user(**credentials)

        # Apply for that job
        application = Application(applicant_id=user2, job_id=job_object)
        application.save()

        response = self.client.post("/profile/selectapplicant", {"job_id": 2, "accept": 2})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="htmx/job-applicants.html")
        self.assertTrue(Application.objects.get(applicant_id=2,job_id=2).status in {"AC", "RE"})

        # At least one application is successful
        self.assertTrue("AC" in [a.status for a in Application.objects.filter(job_id=2)])


class JobDoneButtonCase(LoginRequiredTestCase):
    """Tests for job done button."""

    def setUp(self):
        # Login from super...
        super().setUp()

        # Write 2 job into the job model
        job = dict()
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = 1
        Job.objects.create(**job)

    def test_page(self):
        # test availability via URL
        response = self.client.get("/profile/jobdone")
        self.assertEqual(response.status_code, 404)

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("jobdone"))
        self.assertEqual(response.status_code, 404)

    def test_page_post_no_job(self):
        # test without sending a job id
        response = self.client.post("/profile/jobdone")
        self.assertEqual(response.status_code, 404)

    def test_page_post_job_not_valid(self):
        # test with a wrong job id
        response = self.client.post("/profile/jobdone", {"job_id": 5})
        self.assertEqual(response.status_code, 404)

    def test_page_post_job_no_application_exists(self):
        # test with an application which does not exist
        response = self.client.post("/profile/jobdone", {"job_id": 2})
        self.assertEqual(response.status_code, 404)

    def test_page_post_job_noone_was_accepted(self):
        # test works
        fake = Faker()

        # Create a new job
        job = dict()
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = 1
        job_object = Job.objects.create(**job)

        # Create a user
        credentials = dict()
        credentials["username"] = fake.unique.name()
        credentials["password"] = "a"
        credentials["last_name"] = lambda: fake.last_name()
        credentials["first_name"] = lambda: fake.first_name()
        credentials["date_of_birth"] = datetime.datetime.now()
        user2 = User.objects.create_user(**credentials)

        # Apply for that job
        application = Application(applicant_id=user2, job_id=job_object)

        response = self.client.post("/profile/jobdone", {"job_id": 2})
        self.assertEqual(response.status_code, 404)

    def test_page_post_job(self):
        # test works
        fake = Faker()

        # Create a new job
        job = dict()
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = 1
        job_object = Job.objects.create(**job)

        # Create a user
        credentials = dict()
        credentials["username"] = fake.unique.name()
        credentials["password"] = "a"
        credentials["last_name"] = lambda: fake.last_name()
        credentials["first_name"] = lambda: fake.first_name()
        credentials["date_of_birth"] = datetime.datetime.now()
        user2 = User.objects.create_user(**credentials)

        # Apply for that job
        application = Application(applicant_id=user2, job_id=job_object)
        application.status = "AC"
        application.save()

        response = self.client.post("/profile/jobdone", {"job_id": 2})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="htmx/job-applicants.html")
        self.assertEqual(Application.objects.get(applicant_id=2,job_id=2).status, "DN")


class AccountSettingsTestCase(LoginRequiredTestCase):
    """Tests for the Account Settings page."""

    # test if the account settings page is reachable and uses the right template
    def test_account_settings(self):
        response = self.client.get(reverse("settings"))
        self.assertEqual(response.status_code, 200)

    def test_account_settings_available_by_name(self):
        response = self.client.get(reverse("settings"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="userprofile/usersettings.html")

class NotificationModelTestCase(TestCase):
    """Tests for Notification model"""

    def setUp(self):
        fake = Faker()

        # create 10 users in the database
        for i in range(10):
            credentials = dict()
            credentials["username"] = fake.unique.name()
            credentials["password"] = "a"
            credentials["last_name"] = lambda: fake.last_name()
            credentials["first_name"] = lambda: fake.first_name()
            credentials["date_of_birth"] = datetime.datetime.now()
            User.objects.create_user(**credentials)
            credentials.clear()

        #create 10 notifications in db
        for i in range(10):
            notifications = dict()
            notifications["user_id"] = User(pk=1)
            notifications["content"] = lambda: fake.text()
            notifications["link"] = lambda: fake.url()
            notifications["seen"] = False

            Notification.objects.create(**notifications)

    def test_retrieve_notification(self):
        notifications = Notification.objects.get(pk=1)
        self.assertEqual(notifications.notification_id, 1)

    def test_create_notification(self):
        fake = Faker()

        len1=len(Notification.objects.all())

        notifications = dict()
        notifications["user_id"] = User(pk=1)
        notifications["content"] = lambda: fake.text()
        notifications["link"] = lambda: fake.url()
        notifications["seen"] = False

        Notification.objects.create(**notifications)

        len2 = len(Notification.objects.all())
        self.assertEqual(len1+1, len2)

    def test_delete_notification(self):
        n = Notification.objects.get(pk=1)
        len1 = len(Notification.objects.all())

        n.delete()

        len2=len(Notification.objects.all())
        self.assertEqual(len1-1, len2)

    # Tests the notif_data function for valid data
    # Will fail if there's a validation error
    def test_correct_data(self):

        created_notification=notif_data()

        raised=False

        try:
            created_notification.full_clean()
        except ValidationError:
            raised=True

        self.assertFalse(raised)

    def test_too_long_content(self):

        created_notification=notif_data()

        created_notification.content = "x"*101

        with self.assertRaises(ValidationError):
            created_notification.full_clean()

    def test_too_long_link(self):

        created_notification=notif_data()

        fake = Faker()

        created_notification.link=fake.url() + "x"*200

        with self.assertRaises(ValidationError):
            created_notification.full_clean()

# Creates an instance in the notifications model when called
def notif_data():
    fake = Faker()
    notifications = dict()
    notifications["user_id"] = User(pk=1)
    notifications["content"] = lambda: fake.text()
    notifications["link"] = fake.url()
    notifications["seen"] = False

    return Notification.objects.create(**notifications)


class ProfileEditTestCase(TestCase):
    """Tests for editing a profile"""

    def test_nothing_entered(self):
        # behaviour if form is empty
        form = ProfileEditForm(data={})

        self.assertEqual(2, len(form.errors))

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required.", form.errors[key][0])

    def test_email_entered(self):
        # behaviour if email is entered and valid
        # there should be less errors thrown
        new_data = {
            "email": "madeup@madeup.com",
        }
        form = ProfileEditForm(new_data)

        # Name must be ok
        self.assertEqual(1, len(form.errors))

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required.", form.errors[key][0])

    def test_biography_entered(self):
        # behaviour if biography is entered and valid
        # there should be less errors thrown
        new_data = {
            "biography": "made up bio",
        }
        form = ProfileEditForm(new_data)

        # Name must be ok
        self.assertEqual(1, len(form.errors))

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required.", form.errors[key][0])

    def test_all_valid_entered(self):
        # behaviour if all data is entered and valid
        # there should be no errors thrown
        new_data = {
            "email": "madeup@madeup.com",
            "biography": "made up bio",
        }
        form = ProfileEditForm(new_data)

        # Name must be ok
        self.assertEqual(0, len(form.errors))

    def test_profane_bio_entered(self):
        # behaviour if bio contains profanity
        # there should be less errors thrown
        new_data = {
            "email": "madeup@madeup.com",
            "biography": "kondums",
        }
        form = ProfileEditForm(new_data)

        # Name must be ok
        self.assertEqual(1, len(form.errors))

        # Checks fields for errors
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("Please remove any profanity/swear words.", form.errors[key][0])


class ProfileEditViewTestCase(LoginRequiredTestCase):
    """Tests for editing a profile, view"""

    def test_edit_details_page(self):
        response = self.client.get("/profile/editprofile")
        self.assertEqual(response.status_code, 200)

    def test_edit_details_page_available_by_name(self):
        response = self.client.get(reverse("editprofile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name="editdetails.html"
        )
