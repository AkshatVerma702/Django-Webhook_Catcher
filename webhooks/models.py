from django.db import models
from django.utils import timezone
import json

# Create your models here.
class WebhookToken(models.Model):
    token = models.UUIDField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

class HttpRequest(models.Model):
    token= models.ForeignKey(
        WebhookToken,
        on_delete=models.CASCADE,
        related_name="requests",
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField("Request Date and Time")
    http_method = models.CharField(max_length=200)
    response_status = models.IntegerField(null=True, blank=True)
    content_type = models.TextField(null=True, blank=True)
    ip_addr = models.GenericIPAddressField(null=True, blank=True)
    headers = models.TextField()
    path = models.CharField(max_length=200)
    query_params = models.TextField(null=True, blank=True)
    request_body = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.http_method} {self.path} @ {self.timestamp}"
    
    @classmethod
    def createEntry(cls, request, token_obj):
        x_frwd = request.META.get("HTTP_X_FORWARDED_FOR")
        entry = cls(
            token = token_obj,
            timestamp = timezone.now(),
            http_method = request.method,
            response_status = 0,
            content_type =request.content_type,
            ip_addr = x_frwd.split(",")[0] if x_frwd else request.META.get("REMOTE_ADDR"),
            headers = json.dumps(dict(request.headers)), 
            path = request.path,
            query_params = json.dumps(request.GET.dict()),
            request_body = request.body.decode("utf-8", errors="ignore")
        )

        return entry

