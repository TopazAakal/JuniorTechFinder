from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class LogoutViewTest(TestCase):
    def setUp(self):
        # create a test client and a test user and log the user in.
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_logout_view(self):
        # send a GET request to the logout view.
        response = self.client.get(reverse('logout'))
        # assert that the HTTP response status code is 302 (a redirect)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))
        # assert that the user is logged out.
        self.assertFalse(response.wsgi_request.user.is_authenticated)
