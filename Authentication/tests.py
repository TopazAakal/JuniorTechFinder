from django.test import Client, RequestFactory, TestCase, tag
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .forms import SignUpForm
from .views import signup_view
from django.contrib.auth import get_user_model

# Test case for the LoginView
class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.home_url = reverse('home')

        # Create a test user for authentication
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword')

    # Test logging in with valid credentials
    @tag('unit-test')
    def test_login_valid_credentials(self):
        response = self.client.post(
            self.login_url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, self.home_url)

    # Test logging in with an invalid username
    @tag('unit-test')
    def test_login_invalid_username(self):
        response = self.client.post(
            self.login_url, {'username': 'invaliduser', 'password': 'testpassword'})
        self.assertContains(response, 'Invalid username or password')

    # Test logging in with an invalid password
    @tag('unit-test')
    def test_login_invalid_password(self):
        response = self.client.post(
            self.login_url, {'username': 'testuser', 'password': 'invalidpassword'})
        self.assertContains(response, 'Invalid username or password')

    # Test accessing the login page with a GET request
    @tag('unit-test')
    def test_login_get_request(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    # Test redirecting a user who is already logged in
    @tag('unit-test')
    def test_login_redirect_already_logged_in_user(self):
        # Log the test user in
        self.client.login(username='testuser', password='testpassword')

        # Try to access the login page
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.home_url)

    # Test submitting an empty login form
    @tag('unit-test')
    def test_login_post_request_with_empty_form(self):
        response = self.client.post(self.login_url, {})
        self.assertContains(response, 'This field is required.')

# Test case for the SignUpForm


class SignUpFormTest(TestCase):

    # Test that email is a required field
    @tag('unit-test')
    def test_form_email_required(self):
        form = SignUpForm(
            {'email': '', 'password1': 'password', 'password2': 'password'})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['email'], ['This field is required.'])

    # Test that the two password fields match
    @tag('unit-test')
    def test_form_passwords_match(self):
        form = SignUpForm({'email': 'test@example.com',
                          'password1': 'password1', 'password2': 'password2'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], [
                         'The two password fields didn’t match.'])

# Test case for the SignUpView
class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()  

        
    # Test that the URL for the signup page exists
    @tag('unit-test')
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    # Test that the URL for the signup page is accessible by name
    @tag('unit-test')
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    # Test that the signup page uses the correct template
    @tag('unit-test')
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    # Test that a user can sign up successfully
    @tag('unit-test')
    def test_signup_valid_form(self):
        
        Group.objects.create(name='Junior')
        junior = Group.objects.get(name='Junior')
        # Send a POST request with valid form data
        response = self.client.post(reverse('signup'), {
            'email': 'test2444@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'A123b123',
            'password2': 'A123b123',
            'role': junior.id
        })

        # Assert that the user is redirected to the home page
        self.assertEqual(response.status_code, 302)

        # Assert that the user is created with the provided email
        user = User.objects.get(email='test2444@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.username, 'test2444@example.com')

        # Assert that the user is added to the specified role/group
        self.assertTrue(user.groups.filter(name='Junior').exists())

    # Test redirect authenticated user
    @tag('unit-test')
    def test_redirect_authenticated_user(self):
        # Create an authenticated user
        user = User.objects.create_user(username='testuser', password='password')
        # Log in the user using the client
        self.client.force_login(user)
        # Call the signup_view
        response = self.client.get(reverse('signup'))
        # Assert that the view redirects to the home page
        self.assertRedirects(response, reverse('home'))
            
            
# Test case for the LogoutView
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

    @tag('unit-test')
    def test_logout_view(self):
        # send a GET request to the logout view.
        response = self.client.get(reverse('logout'))
        # assert that the HTTP response status code is 302 (a redirect)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))
        # assert that the user is logged out.
        self.assertFalse(response.wsgi_request.user.is_authenticated)
