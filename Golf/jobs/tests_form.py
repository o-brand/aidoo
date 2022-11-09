

class PostPageCase(TestCase):

    def test_postPage(self):
        self.assertTemplateUsed(response, template_name='postjob.html')
    
class PostJobCase(TestCase):
    def test_post(self):
        new_form = {
            'job_title' : 'Tob'
            'job_short_description' : 'write the tests for me'
            'job_long_description' : 'This is a cry for help, I actually have no skills of writing tests, but wanted to do it on my own cause i wanna learn.'
            'location' : 'AB25 1GN'
            #what? how do I test a checkbox field
        }
        response = self.client.post(reverse('postjob'), data = new_form)

        self.assertEqual(response.statuc_code, 302)

class RegisterFormTestCase(TestCase):
    def test_empty_form(self):
        form = JobForm(data={})

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn('This field is required', form.errors[key][0])

    #ok, this is too much on me