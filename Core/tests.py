
from django.test import TestCase

class AboutUsPageTestCase(TestCase):
    def test_about_us_page(self):
        response = self.client.get('/aboutUs/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aboutUs.html')

class ContactUsPageTestCase(TestCase):
    def test_contact_us_page(self):
        response = self.client.get('/contactUs/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contactUs.html')