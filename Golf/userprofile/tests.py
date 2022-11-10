from Golf.utils import LoginRequiredTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker
import datetime

User = get_user_model() # Get user model

# Testing the User Model
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
            credentials['date_of_birth'] = datetime.datetime.now()
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
        credentials['date_of_birth'] = datetime.datetime.now()
        User.objects.create_user(**credentials)

        len2 = len(User.objects.all())

        self.assertEqual(len1+1, len2)

    def test_delete_user(self):
        u = User.objects.get(pk=1)
        len1 = len(User.objects.all())

        u.delete()

        len2 = len(User.objects.all())

        self.assertEqual(len1-1, len2)


# Tests for the PUBLIC profile page.
class PublicProfileTestCase(LoginRequiredTestCase):

    def test_profile(self):
        response = self.client.get('/profile/' + str(self.user.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='userprofile/public.html')

    def test_profile_available_by_name(self):
        response = self.client.get(reverse('userdetail', kwargs={'user_id':self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_profile_404(self):
        response = self.client.get('/profile/0/')
        self.assertEqual(response.status_code, 404)


# Tests for the PRIVATE profile page.
class PrivateProfileTestCase(LoginRequiredTestCase):

    def test_profile(self):
        response = self.client.get('/profile/me/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='userprofile/private.html')

    def test_profile_available_by_name(self):
        response = self.client.get(reverse('me'))
        self.assertEqual(response.status_code, 200)
