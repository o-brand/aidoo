from django.test import TestCase
from django.contrib.auth.models import User
from jobs.models import JobPosting
from faker import Faker
import random

class UserTableTestCase(TestCase):

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

    def test_retrieve_user(self):

        u = User.objects.get(pk=1)

        self.assertEqual(u.id, 1)

    def test_create_user(self):
        len1 = len(User.objects.all())

        credentials = dict()
        credentials['username'] = '123'
        credentials['password'] = 'a'
        credentials['last_name'] = lambda: fake.last_name()
        credentials['first_name'] = lambda: fake.first_name()
        User.objects.create_user(**credentials)

        len2 = len(User.objects.all())

        self.assertEqual(len1+1, len2)

    def test_delete_user(self):
        u = User.objects.get(pk=1)
        len1 = len(User.objects.all())

        u.delete()

        len2 = len(User.objects.all())

        self.assertEqual(len1-1, len2)

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
            #JobPosting.objects.create_jobPosting()
            jobs = dict()
            jobs['posting_time'] = fake.date()
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

        job['posting_time'] = fake.date()
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



