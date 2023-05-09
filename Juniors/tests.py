from django.test import TestCase, Client
from django.urls import reverse
from Juniors.models import Juniors
from Juniors.forms import JuniorForm
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import resolve_url


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
        response = self.client.get(reverse('createProfile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createProfile.html')
        self.assertIsInstance(response.context['form'], JuniorForm)

    def test_create_profile_POST_valid(self):

        # create a valid form data dictionary
        form_data = {
            'full_name': 'Test User',
            'email': 'testuser@test.com',
            'phone_number': '1234567890',
            'city': 'Test City',
            'age': 25,
            'skills': 'Test Skills',
            'summary': 'Test Summary',
        }

        # create a valid POST request with the form data
        response = self.client.post(reverse('createProfile'), data=form_data)

        # check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # check that the new Junior instance was created in the database
        self.assertEqual(Juniors.objects.count(), 1)

        # check that the new Junior instance has the correct attributes
        junior = Juniors.objects.first()
        self.assertEqual(junior.full_name, 'Test User')
        self.assertEqual(junior.email, 'testuser@test.com')
        self.assertEqual(junior.phone_number, '1234567890')
        self.assertEqual(junior.city, 'Test City')
        self.assertEqual(junior.age, 25)
        self.assertEqual(junior.skills, 'Test Skills')
        self.assertEqual(junior.summary, 'Test Summary')

    def test_create_profile_POST_invalid(self):
        # create an invalid form data dictionary
        form_data = {
            'full_name': 'Test User',
            'email': '',  # invalid email address
            'phone_number': '123456789',  # phone number is too short
            'city': '',  # city field is required
            'age': -1,  # age is negative
            'skills': 'Test Skills',
            'summary': 'Test Summary'
        }

        # create a POST request with the invalid form data
        response = self.client.post(reverse('createProfile'), data=form_data)

        # check that the response status code is 200 (form submission failed)
        self.assertEqual(response.status_code, 200)

        # check that the new Junior instance was not created in the database
        self.assertEqual(Juniors.objects.count(), 0)


class ShowProfileTestCase(TestCase):
    def setUp(self):
        # create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass'
        )

        # create a Junior instance associated with the User
        self.junior = Juniors.objects.create(
            # set the user_id field to the ID of the User instance
            user_id=self.user.id,
            full_name='Test User',
            email='testuser@test.com',
            phone_number='1234567890',
            city='Test City',
            age=25,
            skills='Test Skills',
            summary='Test Summary',
        )

        # log in as the user
        self.client.login(username='testuser', password='testpass')

    def test_showProfile_GET_valid(self):
        # send a GET request to the showProfile view
        response = self.client.get(
            reverse('showProfile', args=[self.junior.pk]))

        # check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # check that the response contains the correct Junior instance
        self.assertEqual(response.context['junior'], self.junior)

    def test_showProfile_GET_invalid(self):
        # send a GET request to the showProfile view with an invalid primary key
        response = self.client.get(
            reverse('showProfile', args=[self.junior.pk + 1]))

        # check that the response status code is 404
        self.assertEqual(response.status_code, 404)


class EditProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass'
        )

        # Fetch the existing "Junior" group
        junior_group = Group.objects.create(name='Junior')
        self.user.groups.add(junior_group)
        self.client.login(username='testuser', password='testpass')

        self.junior = Juniors.objects.create(
            user_id=self.user.id,
            full_name='Test User',
            email='testuser@test.com',
            phone_number='1234567890',
            city='Test City',
            age=25,
            skills='Test Skills',
            summary='Test Summary',
        )
        self.url = reverse('editProfile', args=[self.junior.pk])

    def test_editProfile_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editProfile.html')
        self.assertIsInstance(response.context['form'], JuniorForm)
        self.assertEqual(response.context['form'].instance, self.junior)

    def test_editProfile_POST_invalid(self):
        data = {
            'full_name': 'New Name',
            'email': 'newemail@test.com',
            'phone_number': 'invalid_number',
            'city': 'New City',
            'age': 26,
            'skills': 'New Skills',
            'summary': 'New Summary',
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.junior.refresh_from_db()
        self.assertNotEqual(self.junior.full_name, data['full_name'])
        self.assertNotEqual(self.junior.email, data['email'])
        self.assertNotEqual(self.junior.phone_number, data['phone_number'])
        self.assertNotEqual(self.junior.city, data['city'])
        self.assertNotEqual(self.junior.age, data['age'])
        self.assertNotEqual(self.junior.skills, data['skills'])
        self.assertNotEqual(self.junior.summary, data['summary'])


class CheckProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass'
        )
        self.junior = Juniors.objects.create(
            user_id=self.user.id,
            full_name='Test User',
            email='testuser@test.com',
            phone_number='1234567890',
            city='Test City',
            age=25,
            skills='Test Skills',
            summary='Test Summary',
        )
        self.client.login(username='testuser', password='testpass')

    def test_checkProfile_GET_existing_profile(self):
        response = self.client.get(reverse('checkProfile'))
        self.assertRedirects(response, reverse(
            'showProfile', args=[self.junior.pk]))

    def test_checkProfile_GET_no_profile(self):
        self.junior.delete()  # Delete the existing profile
        response = self.client.get(reverse('checkProfile'))
        self.assertRedirects(response, reverse('createProfile'))
