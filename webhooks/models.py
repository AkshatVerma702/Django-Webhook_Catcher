from django.db import models

# Create your models here.
class HttpRequest(models.Model):
    timestamp = models.DateTimeField("Request Date and Time")
    http_method = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    headers = models.TextField()
    request_body = models.TextField()

    def __str__(self):
        return f"{self.http_method} {self.path} @ {self.timestamp}"