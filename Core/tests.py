from django.test import TestCase, Client
from django.urls import reverse
import logging


class AboutUsPageTestCase(TestCase):
    def test_about_us_page(self):
        response = self.client.get('/aboutUs/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'aboutUs.html')


class ContactUsPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contactUs')

    def test_contact_us_page(self):
        response = self.client.post(self.url, {
            'name': 'Test Test',
            'email': 'test@example.com',
            'message': 'Hello, this is a test message.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Your message has been sent successfully!')

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        expected_output = 'Name: Test Test\nEmail: test@example.com\nMessage: Hello, this is a test message.'
        with self.assertLogs(logger=logger, level='INFO') as cm:
            logger.info(expected_output)
        self.assertIn(expected_output, cm.output[0])
