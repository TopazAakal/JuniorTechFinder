from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.home_url = reverse('home')

        # Create a test user for authentication
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword')

    # Test logging in with valid credentials
    def test_login_valid_credentials(self):
        response = self.client.post(
            self.login_url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, self.home_url)

    # Test logging in with an invalid username
    def test_login_invalid_username(self):
        response = self.client.post(
            self.login_url, {'username': 'invaliduser', 'password': 'testpassword'})
        self.assertContains(response, 'Invalid username or password')

    # Test logging in with an invalid password
    def test_login_invalid_password(self):
        response = self.client.post(
            self.login_url, {'username': 'testuser', 'password': 'invalidpassword'})
        self.assertContains(response, 'Invalid username or password')

    # Test accessing the login page with a GET request
    def test_login_get_request(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    # Test redirecting a user who is already logged in
    def test_login_redirect_already_logged_in_user(self):
        # Log the test user in
        self.client.login(username='testuser', password='testpassword')

        # Try to access the login page
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.home_url)

    # Test submitting an empty login form
    def test_login_post_request_with_empty_form(self):
        response = self.client.post(self.login_url, {})
        self.assertContains(response, 'This field is required.')
