from django.contrib.auth.models import User
from django.test import TestCase, Client, tag
from django.urls import reverse
from Recruiters.models import Interest,JobListing,Recruiters

class ReportsPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', password='admin')
        self.non_admin_user = User.objects.create_user(username='user', password='user')
        
        self.recruiter = Recruiters.objects.create(
            user=self.admin_user,
            full_name='John Doe',
            email='john@example.com',
            phone_number='1234567890',
            city='New York',
            age=30,
            company='ABC Company',
            summary='Recruiter summary',
            photo=None
        )
        
        self.job_listing = JobListing.objects.create(
            title='Job Title',
            description='Job Description',
            requirements='Job Requirements',
            company='XYZ Company',
            location='Chicago',
            recruiter=self.recruiter,
            application_link='https://example.com',
            company_name='XYZ Company',
            salary=50000,
            job_type='Full-time'
        )
        
        self.interest1 = Interest.objects.create(
            name='John Smith',
            email='johnsmith@example.com',
            phone='9876543210',
            resume=None,
            job=self.job_listing,
            status='hired'
        )
        self.interest2 = Interest.objects.create(
            name='Jane Johnson',
            email='janejohnson@example.com',
            phone='1231231234',
            resume=None,
            job=self.job_listing,
            status='rejected'
        )
        
        self.url = reverse('reports') 

    @tag('unit-test')
    def test_admin_access(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports.html')
        self.assertIn('all_Status', response.context)
        all_status = response.context['all_Status']
        self.assertEqual(all_status.count(), 2)

    @tag('unit-test')
    def test_non_admin_access(self):
        self.client.force_login(self.non_admin_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home')) 
