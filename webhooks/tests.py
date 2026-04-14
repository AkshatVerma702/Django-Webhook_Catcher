from django.test import TestCase
from django.urls import reverse
from .models import HttpRequest
from django.utils import timezone
from datetime import timedelta

# Create your tests here.
class HealthTestCase(TestCase):
    def test_health_check(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 200)
    
    def test_homepage(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_catch_hit_success(self):
        response = self.client.get(reverse('generateToken'))
        self.assertEqual(response.status_code, 200)

    def test_model_creation(self):
        initial_count = HttpRequest.objects.count()
        HttpRequest.objects.create(
            timestamp=timezone.now(),
            http_method="GET",
            response_status=200,
            content_type="application/json",
            ip_addr="127.0.0.1",
            headers="User-Agent: TestClient",
            path="/test-url/",
            query_params="page=1",
            request_body=""
        )

        record_count = HttpRequest.objects.count()

        self.assertEqual(record_count - initial_count, 1)


    def test_id_exists(self):
        request_obj = HttpRequest.objects.create(
            timestamp=timezone.now(),
            http_method="GET",
            response_status=200,
            content_type="application/json",
            ip_addr="127.0.0.1",
            headers="User-Agent: TestClient",
            path="/test-url/",
            query_params="page=1",
            request_body=""
        )

        response = self.client.get(reverse('getRequest', kwargs={'target_id': request_obj.id}))

        self.assertEqual(response.status_code, 200)

    def test_filter_logic(self):
        self.filter_logic_data()
        url = reverse('getAllRequests')
        response = self.client.get(url, {'Method': "GET", "Status Code": "200"})

        self.assertEqual(len(response.context["records"]), 2)

    def filter_logic_data(self):
        # create GET method data(2)
        for _ in range(2):
            HttpRequest.objects.create(
                timestamp=timezone.now(),
                http_method="GET",
                response_status=200,
                content_type="application/json",
                ip_addr="127.0.0.1",
                headers="User-Agent: TestClient",
                path="/test-url/",
                query_params="page=1",
                request_body=""
            )
        # Create POST method data
        for _ in range(2):
            HttpRequest.objects.create(
                timestamp=timezone.now(),
                http_method="POST",
                response_status=200,
                content_type="application/json",
                ip_addr="127.0.0.1",
                headers="User-Agent: TestClient",
                path="/test-url/",
                query_params="page=1",
                request_body=""
            )       

    def test_sorting_list(self):
        self.sorting_logic_data()
        url = reverse('getAllRequests')
        response = self.client.get(url, {"sort": "timestamp_asc"})
        result = response.context["records"][0]
        self.assertEqual(result.request_body, "early")

    def sorting_logic_data(self):
        HttpRequest.objects.create(
            timestamp=timezone.now() + timedelta(hours=1),
            http_method="POST",
            response_status=200,
            content_type="application/json",
            ip_addr="127.0.0.1",
            headers="User-Agent: TestClient",
            path="/test-url/",
            query_params="page=1",
            request_body="early"
        )

        HttpRequest.objects.create(
            timestamp=timezone.now() - timedelta(hours=1),
            http_method="GET",
            response_status=200,
            content_type="application/json",
            ip_addr="127.0.0.1",
            headers="User-Agent: TestClient",
            path="/test-url/",
            query_params="page=1",
            request_body="later"
        )

    def create_pagination_data(self):
        for _ in range(6):
            HttpRequest.objects.create(
                timestamp=timezone.now() - timedelta(hours=1),
                http_method="GET",
                response_status=200,
                content_type="application/json",
                ip_addr="127.0.0.1",
                headers="User-Agent: TestClient",
                path="/test-url/",
                query_params="page=1",
                request_body="later"    
            )
    
    def test_pagination_logic(self):
        self.create_pagination_data()
        response = self.client.get(reverse('getAllRequests'), {"page": 1})
        self.assertEqual(len(response.context["page_obj"]), 5)
    
    def test_detail_view(self):
        obj = HttpRequest.objects.create(
            timestamp=timezone.now() - timedelta(hours=1),
            http_method="GET",
            response_status=200,
            content_type="application/json",
            ip_addr="127.0.0.1",
            headers="User-Agent: TestClient",
            path="/test-url/",
            query_params="page=1",
            request_body="later"
        )
        response = self.client.get(reverse("getRequest", kwargs= {"target_id": obj.id}))
        self.assertEqual(len(response.context["records"]), 1)
        self.assertEqual(response.status_code, 200)

    def test_list_view(self):
        self.create_pagination_data()
        response = self.client.get(reverse("getAllRequests"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["records"]), 5)
        self.assertTrue(response.context["page_obj"].has_next())
    
    def test_delete_all(self):
        self.create_pagination_data()

        response = self.client.post(reverse("delete_all"))
        self.assertEqual(HttpRequest.objects.count(), 0)
    
    def test_update_requests_api(self):
        self.create_pagination_data()
        response = self.client.get(reverse("updateView"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
    
    def test_invalid_request_id(self):
        response = self.client.get(reverse("getRequest", kwargs={"target_id" : 9999}))
        self.assertNotEqual(response.status_code, 200)
    
    def test_empty_filter(self):
        response = self.client.get(reverse("getAllRequests"), {"Method": ""})
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_filter(self):
        response = self.client.get(reverse("getAllRequests"), {"Method": "INVALID"})
        self.assertEqual(len(response.context["records"]), 0)
    
    def test_generate_token(self):
        response = self.client.post(reverse("generateToken"))
        self.assertEqual(response.status_code, 200)

    def test_webhook_valid_token(self):
        token_response = self.client.post(reverse("generateToken"))
        token = token_response.json()["token"]
        response = self.client.get(f"/webhook/{token}")
        self.assertEqual(response.status_code, 200)
    
    def test_webhook_invalid_token(self):
        response = self.client.get("/webhook/invalid-token")
        self.assertNotEqual(response.status_code, 200)