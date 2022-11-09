from django.test import TestCase
from userprofile.models import User
import datetime
from django.contrib.auth import get_user_model

User = get_user_model() # Get user model

class LoginRequiredTestCase(TestCase):

    def setUp(self):
        credentials = {
            'username': 'asd',
            'password': 'asd123',
            'date_of_birth':datetime.datetime.now(),
        }
        self.user = User.objects.create_user(**credentials)
        self.client.post('/login/', credentials, follow=True)
