from django.test import TestCase
from django.urls import reverse

class SimpleTest(TestCase):
    # Test case to check the home page status
    def test_home_page(self):
        # Reverse is used to fetch the URL by its name
        url = reverse('routeplanner')  # 'home' is the name of the URL you want to test
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Expect a 200 OK status

    def test_addition(self):
        # Simple test to check basic functionality
        self.assertEqual(1 + 1, 2)  # Should pass

