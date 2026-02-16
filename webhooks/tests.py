from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class HealthTestCase(TestCase):
    def test_health_check(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 200)
    
    def test_catch_hit_success(self):
        response = self.client.get(reverse('catchRequests'))
        self.assertEqual(response.status_code, 200)
    
    def test_request_hit_failure(self):
        response =self.client.get(reverse('getRequest', kwargs={'target_id': 1}))
        self.assertEqual(response.status_code, 200)
    
