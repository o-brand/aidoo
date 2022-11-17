from django.test import TestCase
from Golf.utils import LoginRequiredTestCase
from jobs.models import Job
from userprofile.models import User
from faker import Faker
import random
from django.utils import timezone
from django.urls import reverse
from .forms import JobForm
import datetime
from django.contrib.auth import get_user_model
from Golf.utils import create_date_string

User = get_user_model() # Get user model

# Testing the Job Model
class JobTableTestCase(TestCase):

    def setUp(self):
        fake = Faker()
        # write 10 users into the table
        for i in range(10):
            credentials = dict()
            credentials['username'] = fake.unique.name()
            credentials['password'] = 'a'
            credentials['last_name'] = lambda: fake.last_name()
            credentials['first_name'] = lambda: fake.first_name()
            credentials['date_of_birth'] = datetime.datetime.now()
            User.objects.create_user(**credentials)
            credentials.clear()
        #write 10 jobs into the job_postings table
        for i in range(10):
            # Timezone aware time to do not have a warning.
            tz = timezone.get_current_timezone()
            timzone_datetime = timezone.make_aware(fake.date_time(), tz, True)

            #Job.objects.create_Job()
            jobs = dict()
            jobs['posting_time'] = timzone_datetime
            jobs['points'] = random.randint(0,100)
            jobs['assigned'] = False
            jobs['completed'] = False
            jobs['poster_id_id'] = random.randint(1,10)
            Job.objects.create(**jobs)

    def test_retrieve_job(self):
        job = Job.objects.get(pk=1)

        self.assertEqual(job.job_id, 1)

    def test_create_job(self):
        fake = Faker()
        len1 = len(Job.objects.all())

        job = dict()

        # Timezone aware time to do not have a warning.
        tz = timezone.get_current_timezone()
        timzone_datetime = timezone.make_aware(fake.date_time(), tz, True)

        job['posting_time'] = timzone_datetime
        job['points'] = random.randint(0,100)
        job['assigned'] = False
        job['completed'] = False
        job['poster_id_id'] = random.randint(1,10)
        Job.objects.create(**job)

        len2 = len(Job.objects.all())
        self.assertEqual(len1+1,len2)

    def test_delete_job(self):
        j = Job.objects.get(pk=1)
        len1 = len(Job.objects.all())
        j.delete()

        len2 = len(Job.objects.all())

        self.assertEqual(len1-1,len2)


# Testing the details page.
class DetailsTestCase(LoginRequiredTestCase):

    # Creating a job before every test. (The database is deleted after the test finishes.)
    def setUp(self):
        super().setUp()
        job = {
            'poster_id': self.user,
            'location': 'AB21 3EW',
            'job_title': 'Walking a dog',
            'job_short_description': 'Please walk my dog',
            'job_description': 'Nothing',
            'points': 10,
        }
        Job.objects.create(**job)

    def test_details(self):
        response = self.client.get('/jobs/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='jobdetails.html')

    def test_details_available_by_name(self):
        response = self.client.get(reverse('jobdetails', kwargs={'job_id':1}))
        self.assertEqual(response.status_code, 200)

    def test_details_404(self):
        response = self.client.get('/jobs/0/') # The id starts with 1, so no job is there with this id.
        self.assertEqual(response.status_code, 404)


# Testing the posting page.
class PostPageCase(LoginRequiredTestCase):

    def test_postPage(self):
        response = self.client.get('/jobs/post/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='postjob.html')

    def test_postPage_available_by_name(self):
        response = self.client.get(reverse('post'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_since_everything_is_correct(self):
        new_form = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'write the tests for me',
            'job_description' : 'This is a cry for help, I actually have no skills of writing tests, but wanted to do it on my own cause i wanna learn.',
            'location' : 'AB25 1GN',
            'duration_days' : '0',
            'duration_hours': '1',
            'deadline': datetime.date.today(),
        }
        response = self.client.post(reverse('post'), data = new_form)
        self.assertEqual(response.status_code, 302)


# Testing the posting form.
class PostJobCase(TestCase):
    # poster_id is already there, so we do not test that part!

    
    # Creating a user before every test. (The database is deleted after the test finishes.)
    def setUp(self):
        credentials = {
            'username': 'asd',
            'password': 'asd123',
            'date_of_birth':datetime.datetime.now(),
        }
        User.objects.create_user(**credentials)


    def test_empty_form(self):
        form = JobForm(data={'poster_id': '1'})

        self.assertEqual(6, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required', form.errors[key][0])

    #adding only first fields (job_title)
    #as job_title and short description are formatted in the same, im testing them together
    def test_added_job_title_short_description(self):
        new_application = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'short'
        }
        form = JobForm(data = new_application)

        #check how many errors
        self.assertEqual(4, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required.', form.errors[key][0])

    def test_long_desc_too_long(self):
        new_application = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'short',
            'job_description' : '!'*1001,
        }
        form = JobForm(data = new_application)
        self.assertEqual(4, len(form.errors)) #2 fields should work, 4 still in error

        #check which field an error
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == 'job_description':
                self.assertIn('Ensure this value has at most 1000 characters', form.errors[key][0])
            else:
                self.assertIn('This field is required.', form.errors[key][0])

    def test_long_desc_too_short(self):
        new_application = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'short',
            'job_description' : '!',
        }
        form = JobForm(data = new_application)
        self.assertEqual(4, len(form.errors))

        #check which field an error
        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == 'job_description':
                self.assertIn('Ensure this value has at least 50 characters', form.errors[key][0])
            else:
                self.assertIn('This field is required.', form.errors[key][0])

    def test_added_long_desc(self):
        new_application = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'short',
            'job_description' : 'l'*50,
        }
        form = JobForm(data=new_application)
        self.assertEqual(3, len(form.errors)) #3 fields should be input ok

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required.', form.errors[key][0])

    def test_ZIP_code_not_valid(self):
        new_application = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'short',
            'job_description' : 'l'*50,
            'location' : '00000000',
        }
        form = JobForm(data = new_application)
        self.assertEqual(3, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == 'location':
                self.assertIn('The postcode format is not valid. You must use capital letters.', form.errors[key][0])
            else:
                self.assertIn('This field is required.', form.errors[key][0])

    def test_added_ZIP(self):
        new_application = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'short',
            'job_description' : 'l'*50,
            'location' : 'AB25 3SR',
        }
        form = JobForm(data = new_application)
        self.assertEqual(2, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required.', form.errors[key][0])

    def test_duration_days_not_valid(self):
        new_application = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'short',
            'job_description' : 'l'*50,
            'location' : 'AB25 3SR',
            'duration_days' : '20',
        }

        form = JobForm(data = new_application)
        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == 'duration_days':
                self.assertIn('Select a valid choice. That choice is not one of the available choices.', form.erros[key][0])
            else:
                self.assertIn('This field is required.', form.errors[key][0])

    def test_duration_hours_not_valid(self):
        new_application = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'short',
            'job_description' : 'l'*50,
            'location' : 'AB25 3SR',
            'duration_hours' : '30',
        }

        form = JobForm(data = new_application)
        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == 'duration_hours':
                self.assertIn('Select a valid choice. That choice is not one of the available choices.', form.erros[key][0])
            else:
                self.assertIn('This field is required.', form.errors[key][0])

    def test_fine(self):
        new_application = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'short',
            'job_description' : 'l'*50,
            'location' : 'AB25 3SR',
            'duration_days' : '0',
            'duration_hours' : '1',
        }
        form = JobForm(data=new_application)
        self.assertEqual(0, len(form.errors))
 
    def test_deadline_fine(self):
        new_application = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'short',
            'job_description' : 'l'*50,
            'location' : 'AB25 3SR',
            'duration_days' : '0',
            'duration_hours' : '1',
            'deadline': create_date_string(0),
        }
        form = JobForm(data=new_application)

        # No errors.
        self.assertEqual(0, len(form.errors))

    def test_deadline_in_past_others_are_fine(self):
        new_application = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'short',
            'job_description' : 'l'*50,
            'location' : 'AB25 3SR',
            'duration_days' : '0',
            'duration_hours' : '1',
            'deadline': create_date_string(5),
        }
        form = JobForm(data=new_application)
        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('is not a valid date. The minimum deadline is today.', form.errors[key][0])

    def test_deadline_too_far_others_are_fine(self):
        new_application = {
            'poster_id': '1',
            'job_title' : 'Job',
            'job_short_description' : 'short',
            'job_description' : 'l'*50,
            'location' : 'AB25 3SR',
            'duration_days' : '0',
            'duration_hours' : '1',
            'deadline': create_date_string(-100),
        }
        form = JobForm(data=new_application)
        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('is not a valid date. The deadline cannot be more than 1 year from now.', form.errors[key][0])
