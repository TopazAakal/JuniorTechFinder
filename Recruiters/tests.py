
from django.test import RequestFactory, TestCase, Client
from django.contrib.messages.storage.fallback import FallbackStorage
from Recruiters.views import Recruiters
from Recruiters.forms import RecruitersForm
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
class CreateProfileTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_create_profile_GET(self):
        response = self.client.get(reverse('createProfileRecruiters'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createProfileRecruiters.html')
        self.assertIsInstance(response.context['form'], RecruitersForm)

    def test_create_profile_POST_valid(self):

        # create a valid form data dictionary
        form_data = {
            'full_name': 'Test User',
            'email': 'testuser@test.com',
            'phone_number': '1234567890',
            'city': 'Test City',
            'age': 25,
            'company': 'Test Skills',
            'summary': 'Test Summary',
        }

        # create a valid POST request with the form data
        response = self.client.post(reverse('createProfileRecruiters'), data=form_data)

        # check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Recruiters.objects.count(), 1)

 
        recruiter = Recruiters.objects.first()
        self.assertEqual(recruiter.full_name, 'Test User')
        self.assertEqual(recruiter.email, 'test1user@test.com')
        self.assertEqual(recruiter.phone_number, '1234567890')
        self.assertEqual(recruiter.city, 'Test City')
        self.assertEqual(recruiter.age, 25)
        self.assertEqual(recruiter.company, 'Test Skills')
        self.assertEqual(recruiter.summary, 'Test Summary')

    def test_create_profile_POST_invalid(self):

        # create an invalid form data dictionary
        form_data = {
            'full_name': 'Test User',
            'email': '',  # invalid email address
            'phone_number': '123456789',  # phone number is too short
            'city': '',  # city field is required
            'age': -1,  # age is negative
            'company': 'Test ',
            'summary': 'Test Summary'
        }

        # create a POST request with the invalid form data
        response = self.client.post(reverse('createProfileRecruiters'), data=form_data)

        # check that the response status code is 200 (form submission failed)
        self.assertEqual(response.status_code, 200)

    
        self.assertEqual(Recruiters.objects.count(), 0)


class ShowProfileTestCase(TestCase):
    def setUp(self):
        self.recruiter = Recruiters.objects.create(
            full_name='Test User',
            email='testuser3@test.com',
            phone_number='1234567890',
            city='Test City',
            age=25,
            company='Test ',
            summary='Test Summary',
            photo=SimpleUploadedFile('photo.jpg', b'test')
        )

        # create a Django test client
        self.client = Client()

    def test_showProfile_GET_valid(self):
        # send a GET request to the showProfile view
        response = self.client.get(
            reverse('showProfileRecruiter', args=[self.recruiter.pk]))
        # check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['recruiter'], self.recruiter)

    def test_showProfile_GET_invalid(self):
        # send a GET request to the showProfile view with an invalid primary key
        response = self.client.get(
            reverse('showProfileRecruiter', args=[self.recruiter.pk + 1]))

        # check that the response status code is 404
        self.assertEqual(response.status_code, 404)
