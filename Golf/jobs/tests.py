from django.test import TestCase
from Golf.utils import LoginRequiredTestCase
from jobs.models import JobPosting
from userprofile.models import User
from faker import Faker
import random
from django.utils import timezone
from django.urls import reverse
from .forms import JobForm
import datetime
from django.contrib.auth import get_user_model

User = get_user_model() # Get user model

# TODO Other Tests...

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

            #JobPosting.objects.create_jobPosting()
            jobs = dict()
            jobs['posting_time'] = timzone_datetime
            jobs['points'] = random.randint(0,100)
            jobs['assigned'] = False
            jobs['completed'] = False
            jobs['poster_id_id'] = random.randint(1,10)
            JobPosting.objects.create(**jobs)

    def test_retrieve_job(self):
        job = JobPosting.objects.get(pk=1)

        self.assertEqual(job.job_id, 1)

    def test_create_job(self):
        fake = Faker()
        len1 = len(JobPosting.objects.all())

        job = dict()

        # Timezone aware time to do not have a warning.
        tz = timezone.get_current_timezone()
        timzone_datetime = timezone.make_aware(fake.date_time(), tz, True)

        job['posting_time'] = timzone_datetime
        job['points'] = random.randint(0,100)
        job['assigned'] = False
        job['completed'] = False
        job['poster_id_id'] = random.randint(1,10)
        JobPosting.objects.create(**job)

        len2 = len(JobPosting.objects.all())
        self.assertEqual(len1+1,len2)

    def test_delete_job(self):
        j = JobPosting.objects.get(pk=1)
        len1 = len(JobPosting.objects.all())
        j.delete()

        len2 = len(JobPosting.objects.all())

        self.assertEqual(len1-1,len2)

class FormTestCase():
    #website tests

    class PostPageCase(LoginRequiredTestCase):

        def test_postPage(self):
            response = self.client.get('jobs/post/')
            #test if the website is there, when it should
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_name='postjob.html')
    
        #check whether the html_code_name fits the url
        def test_welcome_available_by_name(self):
            response = self.client.get(reverse('post'))
            self.assertEqual(response.status_code, 200)


    #form tests    
    class PostJobCase(TestCase):
        def test_post(self):
            new_form = {
                'job_title' : 'Job',
                'job_short_description' : 'write the tests for me',
                'job_long_description' : 'This is a cry for help, I actually have no skills of writing tests, but wanted to do it on my own cause i wanna learn.',
                'location' : 'AB25 1GN',
                'duration_days' : '0',
                'duration_hours': '1', 
                
            }
            response = self.client.post(reverse('postjob'), data = new_form)

            #302 is redirect - test whether redirection works
            self.assertEqual(response.status_code, 302)

    class RegisterFormTestCase(TestCase):
        #for testing error messages

        #runserver -> input wrong data -> write test for the error that comes up


        #nothing has been input -> so you need to give error that the field is required
        def test_empty_form(self):
            form = JobForm(data={})

            for key in form.errors:
                error_now = form.errors[key]
                self.assertEqual(1, len(error_now))
                self.assertIn('This field is required', form.errors[key][0])

        #adding only first fields (job_title)
            #as job_title and short description are formatted in the same, im testing them together
        def test_added_job_title(self):
            new_application = {
                'job_title' : 'Job',
                'job_short_description' : 'short'
            }
            form = JobForm(data = new_application)

            self.assertAlmostEqual(4, len(form.errors)) 
            #there are only 4 remaining error fields, as 2 should be input
        #you should have 2 less error message

            #check how many errors
            for key in form.errors:
                error_now = form.errors[key]
                self.assertEqual(1, len(error_now))
                self.assertIn('This field is required.', form.errors[key][0])

        def test_long_desc_too_long(self):
            new_application = {
                'job_title' : 'Job',
                'job_short_description' : 'short', 
                'job_long_description' : '!'*1001,
            }
            form = JobForm(data = new_application)
            self.assertEqual(4, len(form.errors)) #2 fields should work, 4 still in error

            #check which field an error
            for key in form.errors:
                error_now = form.erros[key]
                self.assertEqual(1, len(error_now))

                if key == 'job_long_description':
                    self.assertIn('Ensure this value has at most 1000 characters.', form.errors[key][0])
                else:
                    self.assertIn('This field is required.', form.errors[key][0])

        def test_long_desc_too_short(self):
            new_application = {
                'job_title' : 'Job',
                'job_short_description' : 'short', 
                'job_long_description' : '!',
            }
            form = JobForm(data = new_application)
            self.assertEqual(4, len(form.errors))

            #check which field an error
            for key in form.errors:
                error_now = form.erros[key]
                self.assertEqual(1, len(error_now))

                if key == 'job_long_description':
                    self.assertIn('Ensure this value has at least 50 characters.', form.errors[key][0])
                else:
                    self.assertIn('This field is required.', form.errors[key][0])

        def test_added_long_desc(self):
            new_application = {
                'job_title' : 'Job',
                'job_short_description' : 'short', 
                'job_long_description' : 'l'*50,              
            }
            form = JobForm(data=new_application)
            self.assertEqual(3, len(form.errors)) #3 fields should be input ok

            for key in form.errors:
                error_now = form.errors[key]
                self.assertEqual(1, len(error_now))
                self.assertIn('This field is required.', form.errors[key][0])
        def test_ZIP_code_valid(self):
            new_application = {
                'job_title' : 'Job',
                'job_short_description' : 'short', 
                'job_long_description' : 'l'*50, 
                'location' : '00000000',
            }
            form = JobForm(data = new_application)
            self.assertEqual(3, len(form.errors))

            for key in form.errors:
                error_now = form.errors[key]
                self.assertEqual(1, len(error_now))

                if key == 'location':
                    self.assertIn('Enter a valid ZIP code', form.erros[key][0])

                else:
                    self.assertIn('This field is required.', form.errors[key][0])

        def test_added_ZIP(self):
            new_application = {
                'job_title' : 'Job',
                'job_short_description' : 'short', 
                'job_long_description' : 'l'*50, 
                'location' : 'AB25 3SR',
            }
            form = JobForm(data = new_application)
            self.assertEqual(2, len(form.errors))
        
        def test_duration_days_valid(self):
            new_application = {
                'job_title' : 'Job',
                'job_short_description' : 'short', 
                'job_long_description' : 'l'*50, 
                'location' : 'AB25 3SR',
                'duration_days' : '20',
            }

            form = JobForm(data = new_application)
            self.assertEqual(2, len(form.add_errors))

            for key in form.errors:
                error_now = form.errors[key]
                self.assertEqual(1, len(error_now))

                if key == 'duration_days':
                    self.assertIn('Days out of bounds, enter value betwen 0-15.', form.erros[key][0])
                else:
                    self.assertIn('This field is required.', form.errors[key][0])
        
        def test_duration_hours_valid(self):
            new_application = {
                'job_title' : 'Job',
                'job_short_description' : 'short', 
                'job_long_description' : 'l'*50, 
                'location' : 'AB25 3SR',
                'duration_hours' : '30',
            }

            form = JobForm(data = new_application)
            self.assertEqual(2, len(form.add_errors))

            for key in form.errors:
                error_now = form.errors[key]
                self.assertEqual(1, len(error_now))

                if key == 'duration_hours':
                    self.assertIn('Hours out of bounds, enter value betwen 0-25.', form.erros[key][0])
                else:
                    self.assertIn('This field is required.', form.errors[key][0])
        def test_added_days_hours(self):
            new_application = {
                'job_title' : 'Job',
                'job_short_description' : 'short', 
                'job_long_description' : 'l'*50, 
                'location' : 'AB25 3SR',
                'duration_days' : '0',
                'duration_hours' : '1',
            }

            form = JobForm(data=new_application)
            self.assertEqual(0, len(form.errors))

