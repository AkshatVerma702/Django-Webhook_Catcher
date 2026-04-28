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
    
    def createMultipleData(n):
        token = WebhookToken.objects.create(
            token=uuid.uuid4(),
            expiry=timezone.now() + timedelta(hours=1),
            is_active=True
        )

        for _ in range(n):
            HttpRequest.objects.create(
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

    def test_request_creation(self):
        record_count = HttpRequest.objects.count()
        self.assertEqual(record_count, 1)
    
    def test_request_deletion(self):
        HttpRequest.objects.all().delete()
        record_count =HttpRequest.objects.count()
        self.assertEqual(record_count, 0)
    
    def test_token_creation(self):
        record_count = WebhookToken.objects.count()
        self.assertEqual(record_count, 1)
    
    def test_token_deletion(self):
        WebhookToken.objects.all().delete()
        record_count = WebhookToken.objects.count()
        self.assertEqual(record_count, 0)
    
    def test_foreign_key(self):
        request = HttpRequest.objects.first()
        token = WebhookToken.objects.first()

        self.assertEqual(request.token, token)
    
    def test_request_deleted_when_token_deleted(self):
        WebhookToken.objects.first().delete()
        self.assertEqual(HttpRequest.objects.count(), 0)

    def test_token_has_related_requests(self):
        token = WebhookToken.objects.first()
        requests = token.requests.all()
        self.assertEqual(requests.count(), 1)
    
    def test_str_method(self):
        request = HttpRequest.objects.first()
        expected_string = f'{request.http_method} {request.path} @ {request.timestamp}'
        self.assertEqual(str(request), expected_string)
    
    