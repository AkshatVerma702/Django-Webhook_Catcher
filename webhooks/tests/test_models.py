from django.test import TestCase
from ..models import HttpRequest, WebhookToken
import uuid
from datetime import timedelta
from django.utils import timezone
import json

class RequestModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create Data for tests
        token = WebhookToken.objects.create(
            token=uuid.uuid4(),
            expiry=timezone.now() + timedelta(hours=1),
            is_active=True
        )

        request = HttpRequest.objects.create(
            token=token,
            timestamp=timezone.now(),
            http_method="POST",
            response_status=200,
            content_type="application/json",
            ip_addr="192.168.1.1",
            headers=json.dumps({
                "Content-Type": "application/json"
            }),
            path="/webhook/test/",
            query_params=json.dumps({
                "page": "1",
                "filter": "active"
            }),
            request_body=json.dumps({
                "name": "Akshat",
                "action": "test"
            })
        )
        return super().setUpTestData()

    def test_record_creation(self):
        record_count = HttpRequest.objects.count()
        self.assertEqual(record_count, 1)
    
    def test_record_deletion(self):
        HttpRequest.objects.all().delete()
        record_count =HttpRequest.objects.count()
        self.assertEqual(record_count, 0)
    
    def test_random(self):
        self.assertEqual(0, 0)