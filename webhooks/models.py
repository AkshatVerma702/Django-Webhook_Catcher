from django.db import models
from django.utils import timezone
import json

# Create your models here.
class HttpRequest(models.Model):
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
    def createEntry(cls, request):
        x_frwd = request.META.get("HTTP_X_FORWARDED_FOR")
        entry = cls(
            timestamp = timezone.now(),
            method = request.method,
            response_status = 0,
            content_type =request.content_type,
            ip_addr = x_frwd.split(",")[0] if x_frwd else request.META.get("REMOTE_ADDR"),
            headers = json.dumps(dict(request.headers)), 
            path = request.path,
            query_params = json.dumps(request.GET.dict()),
            body = request.body.decode("utf-8", errors="ignore")
        )
        entry.save()

        return entry