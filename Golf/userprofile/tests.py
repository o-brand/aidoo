from Golf.utils import LoginRequiredTestCase
from django.contrib.auth.models import User
from django.urls import reverse

class ProfileTestCase(LoginRequiredTestCase):

    def test_profile(self):
        response = self.client.get('/profile/' + str(self.user.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='userprofile/profile.html')

    def test_profile_available_by_name(self):
        response = self.client.get(reverse('userdetail', kwargs={'user_id':self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_profile_404(self):
        response = self.client.get('/profile/0/')
        self.assertEqual(response.status_code, 404)
