
from django.test import RequestFactory, TestCase
from django.contrib.messages.storage.fallback import FallbackStorage
from .views import createProfile
from .forms import JuniorForm


class CreateProfileTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_create_profile_valid_form(self):
        # create a dict of valid form data to be used in the test
        data = {
            'full_name': 'John Test',
            'email': 'john.test@example.com',
            'phone_number': '1234567890',
            'city': 'Tel Aviv',
            'age': '25',
            'skills': 'Team work, Python, JavaScript',
            'summary': 'A junior developer with experience in web development',
            'cv_file': 'path/to/cv.pdf',
            'photo': 'path/to/photo.jpg',
        }
        # create a POST request with the form data
        request = self.factory.post('/create_profile/', data)
        # create a JuniorForm object with the POST data and files from the request object
        form = JuniorForm(request.POST, request.FILES)
        # create a session object and attach it to the request object
        request.session = {}
        # create a message storage object and attach it to the request object
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # call the view function with the request object and store the response object
        response = createProfile(request)
        # assert that the response status code is 302 (a redirect)
        self.assertEqual(response.status_code, 302)  # expect redirect

    def test_create_profile_invalid_form(self):
        # create a dict of invalid form data to be used in the test
        data = {
            'full_name': '',  # invalid
            'email': '',  # invalid
            'phone_number': '123',  # invalid
            'city': 'Tel Aviv',
            'age': '-1',  # invalid
            'skills': 'Team work, Python, JavaScript',
            'summary': 'A junior developer with experience in web development',
            'cv_file': 'path/to/cv.txt',  # invalid
            'photo': 'path/to/photo.pdf',  # invalid
        }
        # create a POST request object with the invalid form data
        request = self.factory.post('/create_profile/', data)
        # create a JuniorForm object with the POST data and files from the request object
        form = JuniorForm(request.POST, request.FILES)
        # create a session object and attach it to the request object
        request.session = {}
        # create a message storage object and attach it to the request object
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # call the createProfile view with the request object and store the response object
        response = createProfile(request)
        # expect to stay on the same page
        self.assertEqual(response.status_code, 200)
        # assert that the response contains the error message "Form is not valid."
        self.assertContains(response, "Form is not valid.")

    def test_create_profile_get(self):
        request = self.factory.get('/create_profile/')
        response = createProfile(request)
        # expect successful GET request
        self.assertEqual(response.status_code, 200)
        # expect form instance in the response context
        self.assertIsInstance(response.context['form'], JuniorForm)
