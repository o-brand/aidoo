from django.test import TestCase
from jobs.models import JobPosting
from django.contrib.auth.models import User
from faker import Faker
import random
from django.utils import timezone

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
