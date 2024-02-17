from django.test import TestCase
from django.urls import reverse

class BaseRegisterTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.user = {
            'username':'testusername',
            'email':'testemail@abv.bg',
            'password1':'testpassword',
            'password2':'testpassword',
        }

        return super().setUp()

class RegisterTest(BaseRegisterTest):
    def test_see_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)