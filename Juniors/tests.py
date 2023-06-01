import os
from django.test import TestCase, Client, tag
from django.urls import reverse
from Juniors.models import Juniors
from Juniors.forms import JuniorForm
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import resolve_url
from Recruiters.models import JobListing, Recruiters
from django.core.files import File
from unittest.mock import patch
from .views import PDF2Text, suggestions, generate_new_suggestions


class CreateProfileTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    @tag('unit-test')
    def test_create_profile_GET(self):
        response = self.client.get(reverse('createProfile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createProfile.html')
        self.assertIsInstance(response.context['form'], JuniorForm)

    @tag('unit-test')
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

    @tag('unit-test')
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

    @tag('unit-test')
    def test_showProfile_GET_valid(self):
        # send a GET request to the showProfile view
        response = self.client.get(
            reverse('showProfile', args=[self.junior.pk]))

        # check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # check that the response contains the correct Junior instance
        self.assertEqual(response.context['junior'], self.junior)

    @tag('unit-test')
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

    @tag('unit-test')
    def test_editProfile_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editProfile.html')
        self.assertIsInstance(response.context['form'], JuniorForm)
        self.assertEqual(response.context['form'].instance, self.junior)

    @tag('unit-test')
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

    @tag('unit-test')
    def test_checkProfile_GET_existing_profile(self):
        response = self.client.get(reverse('checkProfile'))
        self.assertRedirects(response, reverse(
            'showProfile', args=[self.junior.pk]))

    @tag('unit-test')
    def test_checkProfile_GET_no_profile(self):
        self.junior.delete()  # Delete the existing profile
        response = self.client.get(reverse('checkProfile'))
        self.assertRedirects(response, reverse('createProfile'))


class JuniorListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.junior1 = Juniors.objects.create(
            user=User.objects.create_user(
                username='testuser1', password='testpassword1'),
            city='City1',
            age=20,
            skills='Skills1'
        )
        self.junior1.photo = File(open('Core/static/media/default.jpg', 'rb'))
        self.junior1.save()

        self.junior2 = Juniors.objects.create(
            user=User.objects.create_user(
                username='testuser2', password='testpassword2'),
            city='City2',
            age=21,
            skills='Skills2'
        )
        self.junior2.photo = File(open('Core/static/media/default.jpg', 'rb'))
        self.junior2.save()

        self.junior3 = Juniors.objects.create(
            user=User.objects.create_user(
                username='testuser3', password='testpassword3'),
            city='City3',
            age=22,
            skills='Skills3'
        )
        self.junior3.photo = File(open('Core/static/media/default.jpg', 'rb'))
        self.junior3.save()

    @tag('unit-test')
    def test_juniorList_GET(self):
        response = self.client.get(reverse('juniorList'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'juniorList.html')
        self.assertCountEqual(response.context['juniors'], [
                              self.junior1, self.junior2, self.junior3])
        self.assertCountEqual(response.context['cities'], [
                              'City1', 'City2', 'City3'])

    @tag('unit-test')
    def test_juniorList_GET_with_skills_filter(self):
        response = self.client.get(
            reverse('juniorList'), {'skills': 'Skills1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'juniorList.html')
        self.assertCountEqual(response.context['juniors'], [self.junior1])
        self.assertCountEqual(response.context['cities'], [
                              'City1', 'City2', 'City3'])

    @tag('unit-test')
    def test_juniorList_GET_with_city_filter(self):
        response = self.client.get(reverse('juniorList'), {'city': 'City2'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'juniorList.html')
        self.assertCountEqual(response.context['juniors'], [self.junior2])
        self.assertCountEqual(response.context['cities'], [
                              'City1', 'City2', 'City3'])

    @tag('unit-test')
    def test_juniorList_GET_with_skills_and_city_filters(self):
        response = self.client.get(reverse('juniorList'), {
                                   'skills': 'Skills1', 'city': 'City1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'juniorList.html')
        self.assertCountEqual(response.context['juniors'], [self.junior1])
        self.assertCountEqual(response.context['cities'], [
                              'City1', 'City2', 'City3'])



class PDF2TextViewTest(TestCase):
    @tag('unit-test')
    def test_pdf2text(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SampleFile.pdf')
        result = PDF2Text(file_path)
        expected_text = "This is a sample PDF file.  \n "
        self.assertEqual(result, expected_text)

class SuggestionsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass'
        )

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

    @tag('unit-test')
    def test_suggestions_get_without_cv_file(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('suggestions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suggestions.html')
        self.assertIn('junior', response.context)
        self.assertEqual(response.context['junior'], self.junior)
        self.assertIn('generated_text', response.context)
        self.assertEqual(response.context['generated_text'], 'Upload your CV to get suggestions')

    @tag('unit-test')
    def test_suggestions_get_with_cv_file(self):
        self.client.force_login(self.user)
        self.junior.cv_file = 'SampleFile.pdf'
        self.junior.save()
        with patch('Juniors.views.PDF2Text') as mock_PDF2Text:
            mock_PDF2Text.return_value = 'Sample CV Text'
            response = self.client.get(reverse('suggestions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suggestions.html')
        self.assertIn('junior', response.context)
        self.assertEqual(response.context['junior'], self.junior)
        self.assertIn('generated_text', response.context)


    @tag('unit-test')
    def test_suggestions_post(self):
        # Prepare the file data
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SampleFile.pdf')
        with open(file_path, 'rb') as file:
            file_data = file.read()
        uploaded_file = SimpleUploadedFile('SampleFile.pdf', file_data, content_type='application/pdf')

        # Send the POST request with the file upload
        response = self.client.post(reverse('suggestions'), {'cv_file': uploaded_file}, format='multipart')
 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'suggestions.html')
        uploaded_file.close()

class GenerateNewSuggestionsViewTest(TestCase):
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
    @tag('unit-test')
    def test_generate_new_suggestions(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('generate_new_suggestions'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('suggestions'))
        self.junior.refresh_from_db()
        self.assertIsNone(self.junior.generated_text)






class JuniorIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.createProfileUrl = reverse('createProfile')
        self.joblist_url = reverse('jobList')

        # Create a recruiter user for adding job list to test job list view
        self.user = User.objects.create_user(
            username='recruiter',
            password='recruiter123'
        )
        recruiter_group = Group.objects.create(name='Recruiter')
        self.user.groups.add(recruiter_group)
        self.client.login(username='recruiter', password='recruiter123')

        self.recruiter = Recruiters.objects.create(
            user=self.user,
            full_name='Test Test',
            email='test@example.com',
            phone_number='1234567890',
            city='test',
            age=40,
            company='Test',
            summary='Test test test',
            photo='01.jpg'
        )

        self.junior_data = {
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': Group.objects.create(name='Junior').id
        }
        self.profile_data = {
            'full_name': 'Test User',
            'email': 'testuser@test.com',
            'phone_number': '1234567890',
            'city': 'Test City',
            'age': 25,
            'skills': 'Test Skills',
            'summary': 'Test Summary',
        }
        # Create an example job listing
        self.job_data = {
            'title': 'Software Engineer',
            'company': 'Example Company',
            'job_type': 'Full-time',
            'location': 'Test City',
            'description': 'Example job description',
            'requirements': 'Example job requirements',
            'salary': 50000,
            'recruiter': self.recruiter,
            'application_link': 'https://example.com/apply',
            'company_name': 'Example Company',
        }
        JobListing.objects.create(**self.job_data)

    @tag('integrationTest')
    def test_Junior_Workflow(self):

        # Signup
        response = self.client.post(self.signup_url, self.junior_data)

        # Redirect after successful signup
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # Login
        response = self.client.post(self.login_url, {
                                    'username': self.junior_data['email'], 'password': self.junior_data['password1']})

        # Redirect after successful login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # Create Profile
        response = self.client.post(self.createProfileUrl, self.profile_data)
        # Redirect after creating profile
        self.assertEqual(response.status_code, 302)

        # View Job List
        response = self.client.get(self.joblist_url)
        self.assertEqual(response.status_code, 200)

        # Check if job listings are displayed
        response = self.client.get(self.joblist_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Software Engineer')
        self.assertContains(response, 'Example Company')

        # Select a Job
        job = JobListing.objects.first()
        job_detail_url = reverse('jobDetail', args=[job.id])
        response = self.client.get(job_detail_url)
        self.assertEqual(response.status_code, 200)

        # Check if the job details are displayed
        self.assertContains(response, job.title)
        self.assertContains(response, job.company_name)
        self.assertContains(response, job.job_type)
        self.assertContains(response, job.location)
