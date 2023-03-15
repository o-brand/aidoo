import datetime
import random
from faker import Faker
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from Golf.utils import create_date_string, fake_time, LoginRequiredTestCase
from .forms import JobForm
from .models import Application, Bookmark, Job
from .validators import validate_deadline, validate_hours, validate_half_hours


# Get actual user model.
User = get_user_model()


class DetailsTestCase(LoginRequiredTestCase):
    """Tests for details page."""

    def setUp(self):
        """Creates a job before every test."""

        # Login from super...
        super().setUp()

        # Create the job
        job = {
            "poster_id": self.user,
            "location": "AB21 3EW",
            "job_title": "Walking a dog",
            "job_description": "Nothing",
            "points": 10,
        }
        Job.objects.create(**job)

    def test_details(self):
        response = self.client.get("/jobs/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="jobdetails.html")

    def test_details_available_by_name(self):
        response = self.client.get(reverse("jobdetails", kwargs={"job_id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_details_404(self):
        # The id starts with 1, so there is no job with this id.
        response = self.client.get("/jobs/0/")
        self.assertEqual(response.status_code, 404)

    def test_details_hidden(self):
        job = {
            "poster_id": self.user,
            "location": "AB21 3EW",
            "job_title": "Walking a dog",
            "job_description": "Nothing",
            "points": 10,
            "hidden": True,
        }
        j = Job.objects.create(**job)

        response = self.client.get("/jobs/" + str(j.job_id) + "/")
        self.assertEqual(response.status_code, 404)


class JobModelTestCase(TestCase):
    """Tests for Job model."""

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
            credentials["profile_id"] = "media/profilepics/default"
            User.objects.create_user(**credentials)
            credentials.clear()

        # Write 10 jobs into the job model
        for i in range(10):
            job = dict()
            job["posting_time"] = fake_time()
            job["points"] = random.randint(0, 100)
            job["assigned"] = False
            job["completed"] = False
            job["poster_id_id"] = random.randint(1, 10)
            Job.objects.create(**job)

    def test_retrieve_job(self):
        # test jobs can be retrieved from the database
        job = Job.objects.get(pk=1)

        self.assertEqual(job.job_id, 1)

    def test_create_job(self):
        # test jobs can be added to the database
        fake = Faker()
        len1 = len(Job.objects.all())

        job = dict()
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = random.randint(1, 10)
        Job.objects.create(**job)

        len2 = len(Job.objects.all())
        self.assertEqual(len1 + 1, len2)

    def test_delete_job(self):
        j = Job.objects.get(pk=1)
        len1 = len(Job.objects.all())

        # Delete the job
        j.delete()

        len2 = len(Job.objects.all())
        self.assertEqual(len1 - 1, len2)

    def test_too_long_location(self):
        job = dict()
        job["location"] = "x" * 9
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = random.randint(1, 10)
        created_job = Job.objects.create(**job)

        with self.assertRaises(ValidationError):
            created_job.full_clean()

    def test_too_long_title(self):
        job = dict()
        job["job_title"] = "x" * 51
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = random.randint(1, 10)
        created_job = Job.objects.create(**job)

        with self.assertRaises(ValidationError):
            created_job.full_clean()

    def test_too_long_job_description(self):
        job = dict()
        job["job_description"] = "x" * 1001
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = random.randint(1, 10)
        created_job = Job.objects.create(**job)

        with self.assertRaises(ValidationError):
            created_job.full_clean()

    def test_too_small_points(self):
        job = dict()
        job["points"] = 0
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = random.randint(1, 10)
        created_job = Job.objects.create(**job)

        with self.assertRaises(ValidationError):
            created_job.full_clean()

    def test_profane_job_title(self):
        job = dict()
        job["job_title"] = "kondums"
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = random.randint(1, 10)
        created_job = Job.objects.create(**job)

        with self.assertRaises(ValidationError):
            created_job.full_clean()

    def test_profane_job_long_description(self):
        job = dict()
        job["job_description"] = " kondums" * 20
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = random.randint(1, 10)
        created_job = Job.objects.create(**job)

        with self.assertRaises(ValidationError):
            created_job.full_clean()


class BookmarkModelTestCase(TestCase):
    """Tests for Bookmark model."""

    def setUp(self):
        fake = Faker()

        # create 1 user in the database
        credentials = dict()
        credentials["username"] = fake.unique.name()
        credentials["password"] = "a"
        credentials["last_name"] = lambda: fake.last_name()
        credentials["first_name"] = lambda: fake.first_name()
        credentials["date_of_birth"] = datetime.datetime.now()
        credentials["profile_id"] = "media/profilepics/default"
        User.objects.create_user(**credentials)
        credentials.clear()

        # Write 1 job into the job model
        job = dict()
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = 1
        Job.objects.create(**job)

    def test_unique_constraint(self):
        """Test if a non-unique user_id and job_id pair raises an error"""
        bookmark = dict()
        bookmark["user_id"] = User(pk=1)
        bookmark["job_id"] = Job(pk=1)
        bookmark["saving_time"] = fake_time()
        Bookmark.objects.create(**bookmark)
        with self.assertRaises(IntegrityError):
            Bookmark.objects.create(**bookmark)


class ApplicationModelTestCasae(TestCase):
    """Test for Application model."""

    def setUp(self):
        fake = Faker()

        #create 1 user in the database
        credentials = dict()
        credentials["username"] = fake.unique.name()
        credentials["password"] = "0"
        credentials["last_name"] = lambda: fake.last_name()
        credentials["first_name"] = lambda: fake.first_name()
        credentials["date_of_birth"] = datetime.datetime.now()
        credentials["profile_id"] = "media/profilepics/default"
        User.objects.create_user(**credentials)
        credentials.clear()

        # Write 1 job into the job model
        job = dict()
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = 1
        Job.objects.create(**job)

    def test_unique_constraint(self):
        application = dict()
        application["applicant_id"] = User(pk=1)
        application["job_id"] = Job(pk=1)
        application["status"] = "AP"  #imo should be AP as it's default
        application["time_of_application"] = fake_time()
        application["time_of_final_status"] = fake_time()

        #creates an object
        Application.objects.create(**application)
        #raise error if duplicate found
        with self.assertRaises(IntegrityError):
            Application.objects.create(**application)


class PostPageCase(LoginRequiredTestCase):
    """Tests for Post page."""

    def test_post_page(self):
        # test availability via URL
        response = self.client.get("/jobs/post")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="postjob.html")

    def test_post_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("post"))
        self.assertEqual(response.status_code, 200)

    def test_no_fund(self):
        # test if the user has no sufficient fund
        new_form = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": ("This is a cry for help, I actually have no "
                "skills of writing tests, but wanted to do it on my own cause "
                "i wanna learn."),
            "location": "AB25 1GN",
            "duration_hours": "8",
            "duration_half_hours": "0",
            "deadline": datetime.date.today(),
        }
        response = self.client.post(reverse("post"), data=new_form)
        self.assertEqual(response.status_code, 200) # No fund error...

    def test_form_not_valid(self):
        # test if the form stays if it has not valid value
        new_form = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": ("This is a cry for help, I actually have no "
                "skills of writing tests, but wanted to do it on my own cause "
                "i wanna learn."),
            "location": "****",
            "duration_hours": "0",
            "duration_half_hours": "0",
            "deadline": datetime.date.today(),
        }
        response = self.client.post(reverse("post"), data=new_form)
        self.assertEqual(response.status_code, 200)

    def test_redirect_since_everything_is_correct(self):
        # test if the user is redirected if the fields are filled in with valid data
        new_form = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": ("This is a cry for help, I actually have no "
                "skills of writing tests, but wanted to do it on my own cause "
                "i wanna learn."),
            "location": "AB25 1GN",
            "duration_hours": "0",
            "duration_half_hours": "0",
            "deadline": datetime.date.today(),
        }
        response = self.client.post(reverse("post"), data=new_form)
        self.assertEqual(response.status_code, 204)


class PostJobCase(TestCase):
    """Tests for posting a job form."""
    # poster_id is already there, so we do not test that part!

    def setUp(self):
        """Creats a user before every test."""
        credentials = {
            "username": "asd",
            "password": "asd123",
            "date_of_birth": datetime.datetime.now(),
            "profile_id": "media/profilepics/default",
        }
        User.objects.create_user(**credentials)

    def test_empty_form(self):
        # behviour if empty form is submitted
        form = JobForm(data={"poster_id": "1"})

        self.assertEqual(5, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required", form.errors[key][0])

    def test_added_job_title_short_description(self):
        new_application = {
            "poster_id": "1",
            "job_title": "Job",
        }
        form = JobForm(data=new_application)

        # check how many errors
        self.assertEqual(4, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required.", form.errors[key][0])

    def test_long_desc_too_long(self):
        # behaviour if long desc too long
        new_application = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": "!" * 1001,
        }
        form = JobForm(data=new_application)

        # 2 fields should work, 4 still in error
        self.assertEqual(4, len(form.errors))

        # check which field an error
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == "job_description":
                self.assertIn(
                    "Ensure this value has at most 1000 characters",
                    form.errors[key][0]
                )
            else:
                self.assertIn("This field is required.", form.errors[key][0])

    def test_long_desc_too_short(self):
        # behaviour if long description too short
        new_application = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": "!",
        }
        form = JobForm(data=new_application)
        self.assertEqual(4, len(form.errors))

        # check which field an error
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == "job_description":
                self.assertIn(
                    "Ensure this value has at least 50 characters",
                    form.errors[key][0]
                )
            else:
                self.assertIn("This field is required.", form.errors[key][0])

    def test_added_long_desc(self):
        # behaviour if long description is correct length
        new_application = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": "l" * 50,
        }
        form = JobForm(data=new_application)

        # 3 fields should be input ok
        self.assertEqual(3, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required.", form.errors[key][0])

    def test_ZIP_code_not_valid(self):
        # behavior if the ZIP code is not valid
        new_application = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": "l" * 50,
            "location": "00000000",
        }
        form = JobForm(data=new_application)
        self.assertEqual(3, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == "location":
                self.assertIn(
                    ("The postcode format is not valid. You must use capital "
                    "letters."),
                    form.errors[key][0],
                )
            else:
                self.assertIn("This field is required.", form.errors[key][0])

    def test_added_ZIP(self):
        # behaviour ZIP code is valid
        new_application = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": "l" * 50,
            "location": "AB25 3SR",
        }
        form = JobForm(data=new_application)
        self.assertEqual(2, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required.", form.errors[key][0])

    def test_duration_hours_not_valid(self):
        # behaviour if the duration is too long
        new_application = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": "l" * 50,
            "location": "AB25 3SR",
            "duration_hours": "20",
            "duration_half_hours": "0",
        }

        form = JobForm(data=new_application)
        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == "duration_hours":
                self.assertIn(
                    ("The number of hours is not valid."),
                    form.errors[key][0],
                )

    def test_duration_half_hours_not_valid(self):
        # behaviour if the duration is too long
        new_application = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": "l" * 50,
            "location": "AB25 3SR",
            "duration_hours": "5",
            "duration_half_hours": "1",
        }

        form = JobForm(data=new_application)
        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == "duration_half_hours":
                self.assertIn(
                    ("The number of minutes is not valid. Only 0 and 30 "
                    "minutes are allowed."),
                    form.errors[key][0],
                )

    def test_fine(self):
        new_application = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": "l" * 50,
            "location": "AB25 3SR",
            "duration_hours": "0",
            "duration_half_hours": "0",
        }
        form = JobForm(data=new_application)
        self.assertEqual(0, len(form.errors))

    def test_deadline_fine(self):
        new_application = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": "l" * 50,
            "location": "AB25 3SR",
            "duration_hours": "0",
            "duration_half_hours": "0",
            "deadline": create_date_string(0),
        }
        form = JobForm(data=new_application)

        # No errors.
        self.assertEqual(0, len(form.errors))

    def test_deadline_in_past_others_are_fine(self):
        new_application = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": "l" * 50,
            "location": "AB25 3SR",
            "duration_hours": "0",
            "duration_half_hours": "0",
            "deadline": create_date_string(5),
        }
        form = JobForm(data=new_application)
        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn(
                "is not a valid date. The minimum deadline is today.",
                form.errors[key][0],
            )

    def test_deadline_too_far_others_are_fine(self):
        new_application = {
            "poster_id": "1",
            "job_title": "Job",
            "job_description": "l" * 50,
            "location": "AB25 3SR",
            "duration_hours": "0",
            "duration_half_hours": "0",
            "deadline": create_date_string(-100),
        }
        form = JobForm(data=new_application)
        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn(
                ("is not a valid date. The deadline cannot be more than 1 "
                "year from now."),
                form.errors[key][0],
            )


class ApplyButtonCase(LoginRequiredTestCase):
    """Tests for apply button."""

    def setUp(self):
        fake = Faker()

        # Login from super...
        super().setUp()

        # Write 1 job into the job model
        job = dict()
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = 1
        Job.objects.create(**job)

    def test_page(self):
        # test availability via URL
        response = self.client.get("/jobs/apply")
        self.assertEqual(response.status_code, 404)

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("apply"))
        self.assertEqual(response.status_code, 404)

    def test_page_post_no_job(self):
        # test without sending a job id
        response = self.client.post("/jobs/apply")
        self.assertEqual(response.status_code, 404)

    def test_page_post_job_not_valid(self):
        # test with a wrong job id
        response = self.client.post("/jobs/apply", {"job_id": 5})
        self.assertEqual(response.status_code, 404)

    def test_page_post_job_application_exists(self):
        # test with an application which exists
        application = dict()
        application["applicant_id"] = User(pk=1)
        application["job_id"] = Job(pk=1)
        application["status"] = "AP"
        Application.objects.create(**application)

        response = self.client.post("/jobs/apply", {"job_id": 1})
        self.assertEqual(response.status_code, 404)

    def test_page_post_job(self):
        # test works
        response = self.client.post("/jobs/apply", {"job_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="htmx/applied.html")
        self.assertEqual(len(Application.objects.all()), 1)


class ReportButtonCase(LoginRequiredTestCase):
    """Tests for report button."""
    # TODO We need to write more tests when the function is fully implemented.

    def setUp(self):
        # Login from super...
        super().setUp()

        # Write 1 job into the job model
        job = dict()
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = 1
        Job.objects.create(**job)

    def test_page(self):
        # test availability via URL
        response = self.client.get("/superadmin/report")
        self.assertEqual(response.status_code, 200)

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("report"))
        self.assertEqual(response.status_code, 200)


class BookmarkButtonCase(LoginRequiredTestCase):
    """Tests for bookmark button."""

    def setUp(self):
        # Login from super...
        super().setUp()

        # Write 1 job into the job model
        job = dict()
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = 1
        Job.objects.create(**job)

    def test_page(self):
        # test availability via URL
        response = self.client.get("/jobs/bookmark")
        self.assertEqual(response.status_code, 404)

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("bookmark"))
        self.assertEqual(response.status_code, 404)

    def test_page_post_no_job(self):
        # test without sending a job id
        response = self.client.post("/jobs/bookmark")
        self.assertEqual(response.status_code, 404)

    def test_page_post_job_not_valid(self):
        # test with a wrong job id
        response = self.client.post("/jobs/bookmark", {"job_id": 5})
        self.assertEqual(response.status_code, 404)

    def test_page_post_job_bookmark_exists(self):
        # test for a bookmarked job (unmarking a job)
        bookmark = dict()
        bookmark["user_id"] = User(pk=1)
        bookmark["job_id"] = Job(pk=1)
        Bookmark.objects.create(**bookmark)

        response = self.client.post("/jobs/bookmark", {"job_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="htmx/bookmark.html")

    def test_page_post_job_bookmark_does_not_exist(self):
        # test for a unmarked job (bookmarking functionality)
        response = self.client.post("/jobs/bookmark", {"job_id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            template_name="htmx/bookmark-unmark.html")


class DeadlineValidationTestCase(TestCase):
    def test_valid_deadline(self):
        """Test a valid deadline date."""
        today = datetime.date.today()
        deadline = today + datetime.timedelta(days=30)  # set deadline 30 days from today
        validate_deadline(deadline)  # should not raise ValidationError

    def test_invalid_past_deadline(self):
        """Test an invalid deadline date in the past."""
        today = datetime.date.today()
        deadline = today - datetime.timedelta(days=1)  # set deadline 1 day in the past
        with self.assertRaises(ValidationError) as cm:
            validate_deadline(deadline)
        self.assertEqual(str(cm.exception), (f"['{deadline} is not a valid "
            "date. The minimum deadline is today.']"))

    def test_invalid_future_deadline(self):
        """Test an invalid deadline date more than 1 year in the future."""
        today = datetime.date.today()
        yearplus = datetime.timedelta(days=400) + datetime.timedelta(days=1)
        deadline = today + yearplus # set deadline more than 1 year in the future
        with self.assertRaises(ValidationError) as cm:
            validate_deadline(deadline)
        self.assertEqual(str(cm.exception), (f"['{deadline} is not a valid "
            "date. The deadline cannot be more than 1 year from now.']"))


class HoursValidationTestCase(TestCase):

    def test_valid_hours(self):
        """Test a valid hour."""
        validate_hours(4)  # should not raise ValidationError

    def test_invalid_hours_too_big(self):
        """Test an invalid hour too big."""
        with self.assertRaises(ValidationError) as cm:
            validate_hours(88)
        self.assertEqual(str(cm.exception), "['The number of hours is not valid.']")

    def test_invalid_hours_too_small(self):
        """Test an invalid hour too small."""
        with self.assertRaises(ValidationError) as cm:
            validate_hours(-2)
        self.assertEqual(str(cm.exception), "['The number of hours is not valid.']")

    def test_invalid_hours_not_integer(self):
        """Test an invalid hour not integer."""
        with self.assertRaises(ValidationError) as cm:
            validate_hours(2.5)
        self.assertEqual(str(cm.exception), "['The number of hours is not valid.']")


class HalfHoursValidationTestCase(TestCase):

    def test_valid_half_hours(self):
        """Test a valid half hour."""
        validate_half_hours(30)  # should not raise ValidationError

    def test_invalid_half_hours(self):
        """Test an invalid half hour."""
        with self.assertRaises(ValidationError) as cm:
            validate_half_hours(23)
        self.assertEqual(str(cm.exception), "['The number of minutes is not valid. Only 0 and 30 minutes are allowed.']")


class CancelButtonCase(LoginRequiredTestCase):
    """Tests for cancel button."""

    def setUp(self):
        fake = Faker()

        # Login from super...
        super().setUp()

        # Write 1 job into the job model
        job = dict()
        job["posting_time"] = fake_time()
        job["points"] = random.randint(0, 100)
        job["assigned"] = False
        job["completed"] = False
        job["poster_id_id"] = 1
        job["hidden"] = False
        Job.objects.create(**job)

    def test_page(self):
        # test availability via URL
        response = self.client.get("/jobs/cancel")
        self.assertEqual(response.status_code, 404)

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("cancel"))
        self.assertEqual(response.status_code, 404)

    def test_page_post_no_job(self):
        # test without sending a job id
        response = self.client.post("/jobs/cancel")
        self.assertEqual(response.status_code, 404)

    def test_page_post_job_not_valid(self):
        # test with a wrong job id
        response = self.client.post("/jobs/cancel", {"job_id": 5})
        self.assertEqual(response.status_code, 404)

    def test_cancel_from_jobs_details(self):
        # Create a new client to imitate a different backstack
        self.client = Client(
            HTTP_REFERER="/jobs/",
        )

        # Login with this client (we already have this user in the db)
        credentials = {
            "username": "asd",
            "password": "asd123",
            "profile_id": "media/profilepics/default",
        }
        self.client.post("/login", credentials, follow=True)

        # Cancel the job
        response = self.client.post("/jobs/cancel", {"job_id": 1})
        
        # The user should get back a response with an extra HTMX attribute
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["HX-Redirect"], "/jobs/")

    def test_cancel_from_profile_page(self):
        # Create a new client to imitate a different backstack
        self.client = Client(
            HTTP_REFERER="/profile/me",
        )

        # Login with this client (we already have this user in the db)
        credentials = {
            "username": "asd",
            "password": "asd123",
            "profile_id": "media/profilepics/default",
        }
        self.client.post("/login", credentials, follow=True)

        # Cancel the job
        response = self.client.post("/jobs/cancel", {"job_id": 1})
        
        # The user should get back a response with an extra HTMX attribute
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["HX-Redirect"], "/profile/me")
