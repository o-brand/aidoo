from django.test import TestCase
from django.contrib.auth.models import User
from userprofile.models import UserExtended
import datetime

class LoginRequiredTestCase(TestCase):

    def setUp(self):
        credentials = {
            'username': 'asd',
            'password': 'asd123'
        }
        self.user = User.objects.create_user(**credentials)
        self.client.post('/login/', credentials, follow=True)

        extended_user = UserExtended(
            user_id=User.objects.get(pk=self.user.id),
            balance=0,
            date_of_birth=datetime.datetime.now(),
            rating=5)
        extended_user.save()
