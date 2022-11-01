from Golf.utils import LoginRequiredTestCase
from django.urls import reverse

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
