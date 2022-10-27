from django.test import TestCase
from django.contrib.auth.models import User

class LoginRequiredTestCase(TestCase):

    def setUp(self):
        credentials = {
            'username': 'asd',
            'password': 'asd123'
        }
        self.user = User.objects.create_user(**credentials)
        self.client.post('/login/', credentials, follow=True)
