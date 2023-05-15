
from django.test import TestCase, Client, RequestFactory, tag
from django.urls import reverse
from Recruiters.models import JobListing, Recruiters
from Recruiters.forms import RecruitersForm
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import RecruitersForm

from Recruiters.views import jobList


class CreateProfileTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser3@test.com',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    @tag('unit-test')
    def test_create_profile_GET(self):
        response = self.client.get(reverse('createProfileRecruiters'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createProfileRecruiters.html')
        self.assertIsInstance(response.context['form'], RecruitersForm)

    @tag('unit-test')
    def test_create_profile_POST_valid(self):

        # create a valid form data dictionary
        form_data = {
            'full_name': 'Test User',
            'email': 'testuser3@test.com',
            'phone_number': '1224567890',
            'city': 'Test City',
            'age': 25,
            'company': 'Test company',
            'summary': 'Test Summary',
        }

        # create a valid POST request with the form data
        response = self.client.post(
            reverse('createProfileRecruiters'), data=form_data)

        # check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Recruiters.objects.count(), 1)

        recruiter = Recruiters.objects.first()
        self.assertEqual(recruiter.full_name, 'Test User')
        self.assertEqual(recruiter.email, 'testuser3@test.com')
        self.assertEqual(recruiter.phone_number, '1224567890')
        self.assertEqual(recruiter.city, 'Test City')
        self.assertEqual(recruiter.age, 25)
        self.assertEqual(recruiter.company, 'Test company')
        self.assertEqual(recruiter.summary, 'Test Summary')

    @tag('unit-test')
    def test_create_profile_POST_invalid(self):

        # create an invalid form data dictionary
        form_data = {
            'full_name': 'Test User',
            'email': '',  # invalid email address
            'phone_number': '1224567890',  # phone number is too short
            'city': '',  # city field is required
            'age': -1,  # age is negative
            'company': 'Test company',
            'summary': 'Test Summary'
        }

        # create a POST request with the invalid form data
        response = self.client.post(
            reverse('createProfileRecruiters'), data=form_data)

        # check that the response status code is 200 (form submission failed)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Recruiters.objects.count(), 0)


class EditProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass'
        )

        recruiter_group = Group.objects.create(name='Recruiter')
        self.user.groups.add(recruiter_group)
        self.client.login(username='testuser', password='testpass')

        self.recruiter = Recruiters.objects.create(
            # set the user_id field to the ID of the User instance
            user_id=self.user.id,
            full_name='Test User',
            email='testuser3@test.com',
            phone_number='1224567890',
            city='Test City',
            age=25,
            company='Test company',
            summary='Test Summary',
            photo='01.jpg',
        )
        self.url = reverse('editProfileRecruiter', kwargs={
                           'pk': self.recruiter.pk})

    @tag('unit-test')
    def test_editProfile_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editProfileRecruiter.html')
        self.assertIsInstance(response.context['form'], RecruitersForm)
        self.assertEqual(response.context['form'].instance, self.recruiter)

    @tag('unit-test')
    def test_editProfile_POST_invalid(self):
        data = {
            'full_name': 'New Name',
            'email': 'newemail@test.com',
            'phone_number': 'invalid_number',
            'city': 'New City',
            'age': 26,
            'company': 'New Company',
            'summary': 'New Summary',
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.recruiter.refresh_from_db()
        self.assertNotEqual(self.recruiter.full_name, data['full_name'])
        self.assertNotEqual(self.recruiter.email, data['email'])
        self.assertNotEqual(self.recruiter.phone_number, data['phone_number'])
        self.assertNotEqual(self.recruiter.city, data['city'])
        self.assertNotEqual(self.recruiter.age, data['age'])
        self.assertNotEqual(self.recruiter.company, data['company'])
        self.assertNotEqual(self.recruiter.summary, data['summary'])


class ShowProfileTestCase(TestCase):
    def setUp(self):
        # create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser3@test.com',
            password='testpass'
        )

        self.recruiter = Recruiters.objects.create(
            # set the user_id field to the ID of the User instance
            user_id=self.user.id,
            full_name='Test User',
            email='testuser3@test.com',
            phone_number='1224567890',
            city='Test City',
            age=25,
            company='Test company',
            summary='Test Summary',
            photo='01.jpg',
        )

        # log in as the user
        self.client.login(username='testuser', password='testpass')

    @tag('unit-test')
    def test_showProfile_GET_valid(self):
        # send a GET request to the showProfile view
        response = self.client.get(
            reverse('showProfileRecruiter', args=[self.recruiter.pk]))

        # check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['recruiter'], self.recruiter)

    @tag('unit-test')
    def test_showProfile_GET_invalid(self):
        # send a GET request to the showProfile view with an invalid primary key
        response = self.client.get(
            reverse('showProfileRecruiter', args=[self.recruiter.pk + 1]))

        # check that the response status code is 404
        self.assertEqual(response.status_code, 404)


class JobListTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        recruiter_group = Group.objects.create(name='Recruiter')
        self.user.groups.add(recruiter_group)
        self.client.login(username='testuser', password='testpass')

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

    @tag('unit-test')
    def test_postJob_view(self):
        url = reverse('postJob')
        # Add the user to the 'Recruiter' group
        recruiter_group = Group.objects.get(name='Recruiter')
        self.user.groups.add(recruiter_group)

        # Log in the user
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'postJob.html')

        form_data = {
            'title': 'Job Title',
            'description': 'Job Description',
            'requirements': 'Job Requirements',
            'company': 'Test Company',
            'location': 'Test Location',
            'application_link': 'https://example.com',
            'company_name': 'Test Company Name',
            'job_type': 'Full-time',
            'recruiter': self.user.pk,
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(JobListing.objects.count(), 1)
        job_listing = JobListing.objects.first()
        self.assertEqual(job_listing.title, 'Job Title')

    @tag('unit-test')
    def test_deleteJob_view(self):
        job_listing = JobListing.objects.create(
            title='Job Title',
            description='Job Description',
            requirements='Job Requirements',
            company='Test Company',
            location='Test Location',
            recruiter=self.recruiter,
            application_link='https://example.com',
            company_name='Test Company Name',
            job_type='Full-time',

        )

        # Add the user to the 'Recruiter' group
        recruiter_group = Group.objects.get(name='Recruiter')
        self.user.groups.add(recruiter_group)

        # Log in the user
        self.client.login(username='testuser', password='testpass123')

        # Perform the delete job request
        response = self.client.post(
            reverse('deleteJob', args=[job_listing.id]))

        # Assert the redirection
        self.assertRedirects(response, reverse(
            'showProfileRecruiter', kwargs={'pk': self.recruiter.pk}))

    @tag('unit-test')
    def test_jobList_view(self):
        url = reverse('jobList')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobList.html')

    @tag('unit-test')
    def test_jobDetail_view(self):
        job_listing = JobListing.objects.create(
            title='Job Title',
            description='Job Description',
            requirements='Job Requirements',
            company='Test Company',
            location='Test Location',
            recruiter=self.recruiter,
            application_link='https://example.com',
            company_name='Test Company Name',
            job_type='Full-time',
        )
        url = reverse('jobDetail', kwargs={'job_id': job_listing.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobDetail.html')
        self.assertEqual(response.context['job'], job_listing)


class RecruiterIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser3@test.com',
            password='testpass'
        )
        recruiter_group = Group.objects.create(name='Recruiter')
        self.user.groups.add(recruiter_group)

        self.client.login(username='testuser', password='testpass')

        self.job_listing_url = reverse('postJob')
        self.profile_url = reverse('createProfileRecruiters')

    @tag('integrationTest')
    def test_recruiter_creation_job_posting(self):
        # create a valid form data dictionary for creating a profile
        profile_form_data = {
            'full_name': 'Test User',
            'email': 'testuser3@test.com',
            'phone_number': '1224567890',
            'city': 'Test City',
            'age': 25,
            'company': 'Test company',
            'summary': 'Test Summary',
        }

        # create a POST request with the form data to create a profile
        profile_response = self.client.post(
            self.profile_url, data=profile_form_data)

        recruiter = Recruiters.objects.first()
        self.assertEqual(recruiter.full_name, 'Test User')
        self.assertEqual(recruiter.email, 'testuser3@test.com')
        self.assertEqual(recruiter.phone_number, '1224567890')
        self.assertEqual(recruiter.city, 'Test City')
        self.assertEqual(recruiter.age, 25)
        self.assertEqual(recruiter.company, 'Test company')
        self.assertEqual(recruiter.summary, 'Test Summary')

        # check that the response status code is 302 (redirect)
        self.assertEqual(profile_response.status_code, 302)

        # create a valid form data dictionary for creating a job listing
        job_listing_form_data = {'title': 'Job Title',
                                 'description': 'Job Description',
                                 'requirements': 'Job Requirements',
                                 'company': 'Test Company',
                                 'location': 'Test Location',
                                 'application_link': 'https://example.com',
                                 'company_name': 'Test Company Name',
                                 'job_type': 'Full-time',
                                 'recruiter': self.user.pk,
                                 }

        # create a POST request with the form data to create a job listing
        job_listing_response = self.client.post(
            self.job_listing_url, data=job_listing_form_data)

        # check that the response status code is 302 (redirect)
        self.assertEqual(job_listing_response.status_code, 302)

        # check that a job listing was created with the correct information
        job_listing = JobListing.objects.first()
        self.assertEqual(job_listing.title, 'Job Title')
        self.assertEqual(job_listing.description, 'Job Description')
        self.assertEqual(job_listing.location, 'Test Location')
        self.assertEqual(job_listing.job_type, 'Full-time')
        self.assertEqual(job_listing.recruiter, recruiter)

        # check that the job listing is associated with the correct recruiter profile
        self.assertIn(job_listing, recruiter.joblisting_set.all())
