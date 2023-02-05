from faker import Faker
import datetime
import random
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.test import TestCase
from Golf.utils import LoginRequiredTestCase
from jobs.models import Job, Application


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

    def fake_time(self):
        """Returns a timezone aware time to prevent warnings."""
        fake = Faker()
        tz = timezone.get_current_timezone()
        return timezone.make_aware(fake.date_time(), tz, True)

    def setUp(self):
        fake = Faker()

        # Login from super...
        super().setUp()

        # Write 1 job into the job model
        for i in range(2):
            job = dict()
            job["posting_time"] = self.fake_time()
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
        self.assertEqual(response.status_code, 204)

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("withdraw"))
        self.assertEqual(response.status_code, 204)

    def test_page_post_no_job(self):
        # test without sending a job id
        response = self.client.post("/profile/withdraw")
        self.assertEqual(response.status_code, 204)

    def test_page_post_job_not_valid(self):
        # test with a wrong job id
        response = self.client.post("/profile/withdraw", {"job_id": 5})
        self.assertEqual(response.status_code, 204)

    def test_page_post_job_does_application_exists(self):
        # test with an application which does not exist
        response = self.client.post("/profile/withdraw", {"job_id": 2})
        self.assertEqual(response.status_code, 204)

    def test_page_post_job(self):
        # test works
        response = self.client.post("/profile/withdraw", {"job_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="htmx/job-applied.html")
        self.assertEqual(Application.objects.get(applicant_id=self.user.id,job_id=1).status, "WD")
